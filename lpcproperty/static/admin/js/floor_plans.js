document.addEventListener("DOMContentLoaded", function () {
    let maxFields = 10;
    let currentField = 1;

    // Get the admin form container
    let adminForm = document.querySelector("#propertymanagement_form");

    if (!adminForm) return; // Exit if the form is not found

    // Find the first floor plan name and image fields
    let firstNameField = document.querySelector('[id^="id_floor_plan_1_name"]');
    let firstImageField = document.querySelector('[id^="id_floor_plan_1_image"]');

    if (!firstNameField || !firstImageField) return; // Exit if fields are missing

    // Create "Add Floor Plan" button
    let addButton = document.createElement('button');
    addButton.innerText = "Add Floor Plan";
    addButton.type = "button";
    addButton.className = "button";
    addButton.style.margin = "10px 0";
    addButton.style.display = "block";

    // Insert the button below the first field
    firstImageField.closest('.form-row').parentNode.appendChild(addButton);

    // Initially hide all extra fields
    for (let i = 2; i <= maxFields; i++) {
        let nameField = document.querySelector(`[id^="id_floor_plan_${i}_name"]`);
        let imageField = document.querySelector(`[id^="id_floor_plan_${i}_image"]`);

        if (nameField && imageField) {
            nameField.closest('.form-row').style.display = "none";
            imageField.closest('.form-row').style.display = "none";
        }
    }

    // Handle button click to show more fields
    addButton.addEventListener("click", function () {
        if (currentField < maxFields) {
            currentField++;
            let nameField = document.querySelector(`[id^="id_floor_plan_${currentField}_name"]`);
            let imageField = document.querySelector(`[id^="id_floor_plan_${currentField}_image"]`);

            if (nameField && imageField) {
                nameField.closest('.form-row').style.display = "block";
                imageField.closest('.form-row').style.display = "block";
            }

            if (currentField === maxFields) {
                addButton.style.display = "none"; // Hide button when max fields are reached
            }
        }
    });
});
