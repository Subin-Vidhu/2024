function changeDate(delta) {
    var dateInput = document.querySelector('input[type="date"]');
    var currentDate = new Date(dateInput.value);
    currentDate.setDate(currentDate.getDate() + delta);
    dateInput.value = currentDate.toISOString().split('T')[0];
}