import { useState } from "react";

function MyEvents({ rollNo }) {
    const [events, setEvents] = useState([]);

    function showEvents() {
    if (rollNo === "") {
        alert("Enter Roll Number");
        return;
    }

    fetch("http://127.0.0.1:8001/registrations/" + rollNo)
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        setEvents(data);
    });
}

    function cancel(id) {
        fetch("http://127.0.0.1:8001/registrations/" + id + "/cancel", {
            method: "PATCH"
        })
        .then(function() {
            showEvents();
        });
    }

    return (
        <>
            <h2>My Events</h2>
            <button onClick={showEvents}>Show</button>

            {events.map(function(item) {
                return (
                    <p key={item.registration_id}>
                        {item.title} - {item.event_date}
                        <button onClick={function() {
                            cancel(item.registration_id);
                        }}>
                            Cancel Event
                        </button>
                    </p>
                );
            })}
        </>
    );
}

export default MyEvents;