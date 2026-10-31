function WardenDashboard() {
    return (
        <div>
            <h2>Warden Dashboard</h2>

            <h3>Complaint Summary</h3>

            <div>
                <p>Open: 0</p>
                <p>In Progress: 0</p>
                <p>Resolved: 0</p>
            </div>

            <h3>Filter Complaints</h3>

            <div>
                <select>
                    <option value="">All Statuses</option>
                    <option value="open">Open</option>
                    <option value="in_progress">In Progress</option>
                    <option value="resolved">Resolved</option>
                </select>

                <select>
                    <option value="">All Categories</option>
                    <option value="electrical">Electrical</option>
                    <option value="plumbing">Plumbing</option>
                    <option value="furniture">Furniture</option>
                    <option value="cleaning">Cleaning</option>
                    <option value="internet">Internet</option>
                </select>
            </div>

            <h3>All Complaints</h3>

        </div>
    );
}

export default WardenDashboard;
