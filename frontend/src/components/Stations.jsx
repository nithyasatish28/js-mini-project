function Stations({ stations, onSelectStation, onBorrow }) {
    return (
        <section className="stations-section">
            <div className="section-heading">
                <div>
                    <span className="eyebrow">CAMPUS NETWORK</span>
                    <h2>Explore Stations</h2>
                    <p>Find an umbrella station near your destination.</p>
                </div>
                <span className="station-count">{stations.length} Stations</span>
            </div>

            <div className="station-grid">
                {stations.map((station) => (
                    <div className="station-card" key={station.id}>
                        <div className="station-card-top">
                            <span className="station-number">STATION {station.id}</span>
                            <span className={`status-badge ${station.umbrellas_available === 0 ? "empty" : station.umbrellas_available === station.capacity ? "full" : "available"}`}>
                                {station.umbrellas_available === 0 ? "Empty" : station.umbrellas_available === station.capacity ? "Full" : "Available"}
                            </span>
                        </div>

                        <div className="station-icon">☂</div>
                        <h3 onClick={() => onSelectStation(station.id)}>{station.name}</h3>
                        <p className="station-location">{station.location}</p>

                        <div className="availability-info">
                            <span>Umbrella availability</span>
                            <strong>{station.umbrellas_available}/{station.capacity}</strong>
                        </div>

                        <div className="progress-track">
                            <div className="progress-fill" style={{ width: `${station.umbrellas_available / station.capacity * 100}%` }}></div>
                        </div>

                        <div className="station-card-bottom">
                            <span>{station.free_slots} free slots</span>
                            <button className="borrow-button" disabled={station.umbrellas_available === 0} onClick={() => onBorrow(station.id)}>
                                Borrow Umbrella →
                            </button>
                        </div>
                    </div>
                ))}
            </div>

            {stations.length === 0 && <p>No stations found.</p>}
        </section>
    );
}

export default Stations;