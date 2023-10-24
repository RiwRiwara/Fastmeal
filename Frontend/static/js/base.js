async function getSession() {
    try {
        const response = await fetch('/view_session');
        if (!response.ok) {
            throw new Error(`Request failed with status: ${response.status}`);
        }
        const data = await response.json();
        return data; 
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}

async function JoinNow() {
    try {
        var ssdata = await getSession();
        console.log(ssdata);
    } catch (error) {
        console.error('Error:', error);
    }
}
