import { createServer } from 'node:http';
import { DatabaseSync } from 'node:sqlite';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const port = Number(process.env.PORT || 8000);
const databasePath = join(dirname(fileURLToPath(import.meta.url)), 'lost_found.db');
const database = new DatabaseSync(databasePath);

database.exec(`
  CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    posted_at DATETIME NOT NULL,
    location VARCHAR,
    status VARCHAR NOT NULL,
    contact VARCHAR NOT NULL,
    resolved_at DATETIME
  )
`);

const selectAll = database.prepare(`
  SELECT id, name, description, posted_at, location, status, contact, resolved_at
  FROM items
  ORDER BY posted_at DESC, id DESC
`);
const selectOne = database.prepare(`
  SELECT id, name, description, posted_at, location, status, contact, resolved_at
  FROM items WHERE id = ?
`);
const insertItem = database.prepare(`
  INSERT INTO items (name, description, posted_at, location, status, contact, resolved_at)
  VALUES (?, ?, ?, ?, 'active', ?, NULL)
`);

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

function validateItem(body) {
  if (!body || typeof body !== 'object' || Array.isArray(body)) {
    return { errors: ['Request body must be a JSON object.'], value: {} };
  }

  const errors = [];
  const value = {};

  for (const [field, maxLength] of [
    ['name', 120],
    ['description', 1000],
    ['contact', 200],
    ['location', 200],
  ]) {
    const rawValue = body[field];
    const fieldValue = rawValue == null ? '' : String(rawValue).trim();
    if (field !== 'location' && !fieldValue) {
      errors.push(`${field} is required.`);
    } else if (fieldValue.length > maxLength) {
      errors.push(`${field} must be ${maxLength} characters or fewer.`);
    } else {
      value[field] = fieldValue || null;
    }
  }

  return { errors, value };
}

function itemPath(pathname) {
  const match = pathname.match(/^\/(?:api\/)?items(?:\/(\d+))?\/?$/);
  if (!match) return null;
  return match[1] ? Number(match[1]) : 0;
}

const server = createServer(async (request, response) => {
  const pathname = new URL(request.url || '/', 'http://localhost').pathname;

  if (request.method === 'GET' && pathname === '/api/health') {
    return sendJson(response, 200, { status: 'ok' });
  }

  const itemId = itemPath(pathname);
  if (itemId === null) {
    return sendJson(response, 404, { detail: 'Route not found.' });
  }

  try {
    if (request.method === 'GET' && itemId === 0) {
      return sendJson(response, 200, selectAll.all());
    }

    if (request.method === 'GET' && itemId > 0) {
      const item = selectOne.get(itemId);
      return item
        ? sendJson(response, 200, item)
        : sendJson(response, 404, { detail: 'Item not found.' });
    }

    if (request.method === 'POST' && itemId === 0) {
      const body = await readJson(request);
      const { errors, value } = validateItem(body);
      if (errors.length) return sendJson(response, 422, { detail: errors });

      const postedAt = new Date().toISOString();
      const result = insertItem.run(
        value.name,
        value.description,
        postedAt,
        value.location,
        value.contact,
      );
      return sendJson(response, 201, selectOne.get(Number(result.lastInsertRowid)));
    }

    response.setHeader('Allow', itemId === 0 ? 'GET, POST' : 'GET');
    return sendJson(response, 405, { detail: 'Method not allowed.' });
  } catch (error) {
    const responseStatus = error.message === 'Request body must be valid JSON.' ? 400 : 500;
    if (responseStatus === 500) console.error('Lost and Found API error:', error);
    return sendJson(response, responseStatus, {
      detail: error.message || 'Internal server error.',
    });
  }
});

server.listen(port, '127.0.0.1', () => {
  console.log(`Lost and Found API listening at http://127.0.0.1:${port}`);
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
