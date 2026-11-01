import { useState } from "react";

function MyEvents({ rollNo }) {
    const [events, setEvents] = useState([]);

    function showEvents() {
    if (rollNo === "") {
        alert("Enter Roll Number");
        return;
    }

    fetch(API_URL/registrations/" + rollNo)
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        setEvents(data);
    });
}

    function cancel(id) {
        fetch(API_URL+ "/registrations/" + id + "/cancel", {
            method: "PATCH"
        })
        .then(function(response) {
            return response.json();
        });
    }

    return (
        <>
            <h2>My Events</h2>
            <button onClick={showEvents}>Show</button>

            {events.map(function(item) {
                return (
                    <p key={item.registration_id}>
                        <p></p>{item.title}<p/>
                        <p>{item.event_date}</p>
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
