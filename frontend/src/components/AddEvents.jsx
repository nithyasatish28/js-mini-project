import API_URL from "../api";
function AddEvent({ getEvents }) {
    function addEvent(event) {
        event.preventDefault();
        fetch(API_URL + "/events", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: event.target.title.value,
                club: event.target.club.value,
                category: event.target.category.value,
                event_date: event.target.event_date.value,
                total_seats: Number(event.target.total_seats.value)
            })
        })
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            alert("Event added");
            getEvents();
        });
    }

    return (
        <>
            <h2>Add Event</h2>

            <form onSubmit={addEvent}>
                <input name="title" placeholder="Event Title" required />
                <input name="club" placeholder="Club" required />
                <input name="category" placeholder="Category" required />
                <input name="event_date" type="date" required />
                <input name="total_seats" type="number" placeholder="Total Seats" required />
                <button type="submit">Add Event</button>
            </form>
        </>
    );
}

export default AddEvent;