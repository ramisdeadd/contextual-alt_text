let SELECTED = []

document.addEventListener("DOMContentLoaded", () => {
    select_checkboxes = document.querySelectorAll('.select-item').forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            if (checkbox.checked) {
                SELECTED.push(checkbox.value)
            } else {
                SELECTED = SELECTED.filter(item => item !== checkbox.value)
            }
        })
    })
})