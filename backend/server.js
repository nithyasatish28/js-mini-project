import { createServer } from 'node:http';
import { DatabaseSync } from 'node:sqlite';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const port = Number(process.env.PORT || 8000);
const databasePath = join(dirname(fileURLToPath(import.meta.url)), 'complaints.db');
const database = new DatabaseSync(databasePath);
const statuses = ['active', 'pending', 'resolved', 'closed'];

database.exec(`
  CREATE TABLE IF NOT EXISTS "Complaints" (
    id INTEGER PRIMARY KEY,
    roll_no INTEGER,
    room_no VARCHAR,
    catagory VARCHAR,
    description VARCHAR,
    status VARCHAR,
    created_on DATETIME,
    resolved_on DATETIME
  )
`);

const selectAll = database.prepare(`
  SELECT id, roll_no, room_no, catagory, description, status, created_on, resolved_on
  FROM "Complaints"
  ORDER BY created_on DESC, id DESC
`);
const selectOne = database.prepare(`
  SELECT id, roll_no, room_no, catagory, description, status, created_on, resolved_on
  FROM "Complaints" WHERE id = ?
`);
const selectByStatus = database.prepare(`
  SELECT id, roll_no, room_no, catagory, description, status, created_on, resolved_on
  FROM "Complaints" WHERE status = ?
  ORDER BY created_on DESC, id DESC
`);
const insertComplaint = database.prepare(`
  INSERT INTO "Complaints" (roll_no, room_no, catagory, description, status, created_on, resolved_on)
  VALUES (?, ?, ?, ?, ?, ?, NULL)
`);
const updateComplaint = database.prepare(`
  UPDATE "Complaints"
  SET roll_no = ?, room_no = ?, catagory = ?, description = ?, status = ?, resolved_on = ?
  WHERE id = ?
`);
const resolveComplaint = database.prepare(`
  UPDATE "Complaints" SET status = 'resolved', resolved_on = ? WHERE id = ?
`);
const deleteComplaint = database.prepare('DELETE FROM "Complaints" WHERE id = ?');

function sendJson(response, responseStatus, data) {
  response.writeHead(responseStatus, {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
  });
  response.end(JSON.stringify(data));
}

function readJson(request) {
  return new Promise((resolve, reject) => {
    let body = '';
    request.on('data', (chunk) => {
      body += chunk;
      if (body.length > 1_000_000) {
        reject(new Error('Request body is too large.'));
        request.destroy();
      }
    });
    request.on('end', () => {
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch {
        reject(new Error('Request body must be valid JSON.'));
      }
    });
    request.on('error', reject);
  });
}

function validateComplaint(body, partial = false) {
  if (!body || typeof body !== 'object' || Array.isArray(body)) {
    return { errors: ['Request body must be a JSON object.'], value: {} };
  }

  const errors = [];
  const value = {};

  if (!partial || Object.hasOwn(body, 'roll_no')) {
    const rollNumber = Number(body.roll_no);
    if (!Number.isSafeInteger(rollNumber) || rollNumber < 1) {
      errors.push('roll_no must be a positive whole number.');
    } else {
      value.roll_no = rollNumber;
    }
  }

  for (const [field, maxLength] of [
    ['room_no', 30],
    ['catagory', 80],
    ['description', 1000],
    ['status', 30],
  ]) {
    if (partial && !Object.hasOwn(body, field)) continue;
    const fieldValue = body[field] == null ? '' : String(body[field]).trim();
    if (field === 'status' && !fieldValue && !partial) {
      value.status = 'active';
      continue;
    }
    if (field === 'room_no' && !fieldValue) {
      errors.push('room_no is required.');
    } else if (field === 'status' && !statuses.includes(fieldValue.toLowerCase())) {
      errors.push(`status must be one of: ${statuses.join(', ')}.`);
    } else if (fieldValue.length > maxLength) {
      errors.push(`${field} must be ${maxLength} characters or fewer.`);
    } else {
      value[field] = field === 'status'
        ? fieldValue.toLowerCase()
        : fieldValue || null;
    }
  }

  return { errors, value };
}

function complaintPath(pathname) {
  const match = pathname.match(/^\/(?:api\/)?complaints(?:\/(\d+))?\/?$/);
  if (!match) return null;
  return match[1] ? Number(match[1]) : 0;
}

const server = createServer(async (request, response) => {
  const pathname = new URL(request.url || '/', 'http://localhost').pathname;

  if (request.method === 'GET' && pathname === '/api/health') {
    return sendJson(response, 200, { status: 'ok' });
  }

  const statusMatch = pathname.match(/^\/(?:api\/)?complaints\/status\/([^/]+)\/?$/);
  const resolveMatch = pathname.match(/^\/(?:api\/)?complaints\/(\d+)\/resolve\/?$/);
  const complaintId = complaintPath(pathname);
  if (complaintId === null && !statusMatch && !resolveMatch) {
    return sendJson(response, 404, { detail: 'Route not found.' });
  }

  try {
    if (request.method === 'GET' && statusMatch) {
      const complaintStatus = decodeURIComponent(statusMatch[1]).toLowerCase();
      if (!statuses.includes(complaintStatus)) {
        return sendJson(response, 400, { detail: `Status must be one of: ${statuses.join(', ')}.` });
      }
      return sendJson(response, 200, selectByStatus.all(complaintStatus));
    }

    if (request.method === 'GET' && complaintId === 0) {
      return sendJson(response, 200, selectAll.all());
    }

    if (request.method === 'GET' && complaintId > 0) {
      const complaint = selectOne.get(complaintId);
      return complaint
        ? sendJson(response, 200, complaint)
        : sendJson(response, 404, { detail: 'Complaint not found.' });
    }

    if (request.method === 'POST' && complaintId === 0) {
      const body = await readJson(request);
      const { errors, value } = validateComplaint(body);
      if (errors.length) return sendJson(response, 422, { detail: errors });

      const result = insertComplaint.run(
        value.roll_no,
        value.room_no,
        value.catagory,
        value.description,
        value.status || 'active',
        new Date().toISOString(),
      );
      if (['resolved', 'closed'].includes((value.status || 'active').toLowerCase())) {
        database.prepare('UPDATE "Complaints" SET resolved_on = ? WHERE id = ?')
          .run(new Date().toISOString(), Number(result.lastInsertRowid));
      }
      return sendJson(response, 201, selectOne.get(Number(result.lastInsertRowid)));
    }

    if (request.method === 'PUT' && complaintId > 0) {
      const existing = selectOne.get(complaintId);
      if (!existing) return sendJson(response, 404, { detail: 'Complaint not found.' });

      const body = await readJson(request);
      const { errors, value } = validateComplaint(body, true);
      if (errors.length) return sendJson(response, 422, { detail: errors });
      if (!Object.keys(value).length) {
        return sendJson(response, 400, { detail: 'Provide at least one field to update.' });
      }

      const updated = { ...existing, ...value };
      if (Object.hasOwn(value, 'status')) {
        updated.resolved_on = ['resolved', 'closed'].includes(updated.status.toLowerCase())
          ? updated.resolved_on || new Date().toISOString()
          : null;
      }
      updateComplaint.run(
        updated.roll_no,
        updated.room_no,
        updated.catagory,
        updated.description,
        updated.status,
        updated.resolved_on,
        complaintId,
      );
      return sendJson(response, 200, selectOne.get(complaintId));
    }

    if (request.method === 'DELETE' && complaintId > 0) {
      const result = deleteComplaint.run(complaintId);
      return result.changes
        ? sendJson(response, 200, { message: 'Complaint deleted successfully' })
        : sendJson(response, 404, { detail: 'Complaint not found.' });
    }

    if (request.method === 'PATCH' && resolveMatch) {
      const resolvedId = Number(resolveMatch[1]);
      if (!selectOne.get(resolvedId)) {
        return sendJson(response, 404, { detail: 'Complaint not found.' });
      }
      resolveComplaint.run(new Date().toISOString(), resolvedId);
      return sendJson(response, 200, selectOne.get(resolvedId));
    }

    if (statusMatch) {
      response.setHeader('Allow', 'GET');
    } else if (resolveMatch) {
      response.setHeader('Allow', 'PATCH');
    } else {
      response.setHeader('Allow', complaintId === 0 ? 'GET, POST' : 'GET, PUT, DELETE');
    }
    return sendJson(response, 405, { detail: 'Method not allowed.' });
  } catch (error) {
    const responseStatus = error.message === 'Request body must be valid JSON.' ? 400 : 500;
    if (responseStatus === 500) console.error('Complaint API error:', error);
    return sendJson(response, responseStatus, {
      detail: error.message || 'Internal server error.',
    });
  }
});

server.listen(port, '127.0.0.1', () => {
  console.log(`Hostel Complaint Tracker API listening at http://127.0.0.1:${port}`);
  console.log(`Using database: ${databasePath}`);
});

function closeServer() {
  server.close(() => {
    database.close();
    process.exit(0);
  });
}

process.on('SIGINT', closeServer);
process.on('SIGTERM', closeServer);
