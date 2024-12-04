var flag = 0; // 'start', ''

displaylog();
const addButton = document.getElementById("addButton");
const addWebsiteModal = document.getElementById("addWebsiteModal");
const closeModal = document.getElementById("closeModal");

// Show the modal when the "Add" button is clicked
addButton.addEventListener("click", () => {
    addWebsiteModal.classList.remove("hidden");
});

// Close the modal when the "Cancel" button is clicked
closeModal.addEventListener("click", () => {
    addWebsiteModal.classList.add("hidden");
});

// Optionally: Close the modal if clicked outside of the modal content
window.addEventListener("click", (event) => {
    if (event.target === addWebsiteModal) {
        addWebsiteModal.classList.add("hidden");
    }
});

const addWebsiteForm = document.getElementById('addWebsiteForm');

addWebsiteForm.addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent the form from submitting normally
    
    // Collect form data
    const formData = new FormData();
    // Send AJAX request to add websites
    let sites = document.getElementById('websites').value;
    formData.append('websites', sites);
    alert(sites)
    fetch("addsite", { //{% url 'add_websites' %}
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.status) {
            addlog(data.result + ' websites successfully added!');
            addWebsiteModal.classList.add('hidden');  // Close the modal
            location.reload();

        } else {
            addlog('server error');
        }
    })
    .catch(error => {
        addlog('There was an error submitting the form', error);
    });
});



const updateButton = document.getElementById('updateButton');

function originButton(){
    flag = false;
    updateButton.innerHTML = "Update";
    if (updateButton.classList.contains('bg-gray-500')) {
        updateButton.classList.remove('bg-gray-500');
        updateButton.classList.add('bg-green-500');
    }
}

function changeCheckbox(disable){
    const checkboxes = document.querySelectorAll('input[name="urlcheckbox"]:checked'); 
    checkboxes.forEach(checkbox => {
        console.log('sdf')
        checkbox.disabled = disable;
    });
}

updateButton.onclick = () => {
    if(flag){
        flag = false;
        changeCheckbox(false)
        originButton();
        addlog("⛔Stop scrapying...\n");
        return;
    }
    const checkboxes = document.querySelectorAll('input[name="urlcheckbox"]:checked'); 
    const selectedUrls = [];  
    checkboxes.forEach((checkbox) => {  
        selectedUrls.push(checkbox.getAttribute('data-url'));  
    }); 
    count = selectedUrls.length;
    if(count == 0){
        addlog("⚠️ Pleas select the websites for updating\n");
        return;
    }
    index = 0;
    flag = true;
    changeCheckbox(true);
    addlog("🚀Start scrapying for selected websites...\n\n");
    updateButton.innerHTML = "Stop Updating";
    if (updateButton.classList.contains('bg-green-500')) {
        updateButton.classList.remove('bg-green-500');
        updateButton.classList.add('bg-gray-500');
    }
    updateOneByOne(index, selectedUrls);
}

function updateOneByOne(index, selectedUrls){
    if(index >= selectedUrls.length){
        originButton();
        addlog("🔚Completed updating!\n");
        changeCheckbox(false);
        return;
    }
    addlog("⚡Starting scrapying for 🌐" + selectedUrls[index] + "🌐\n");
    if(!flag){  
        addlog("✋Scraping Stopped By User\n");
        changeCheckbox(false);
        return;
    }
    const formData = new FormData();
    try{
        formData.append('website', selectedUrls[index]);
        fetch("updatesite", { //{% url 'update_websites' %}
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            if(data.status){
                console.log(data)
                let log = '';
                log += "Successfully completed scrapying for website 🌐" + data.result[0] + "🌐\n";
                log += "                Chunk Count is " + data.result[1] + "\n";
                log += "                Updated Date is " + data.result[2];
                addlog(log);
            }
            else{
                let log = '';
                log += "Failed with scrapying for website " + selectedUrls[index] + "\n";
                log += "Error occured " + data.message+ "\n";
                addlog(log)
            }
            updateOneByOne(index + 1, selectedUrls)
        })
        .catch(error => {
            addlog("Successfully completed scrapying for website 🌐" + data.result[0] + "🌐\n");
            alert('Failed to update selected websites.');
            updateOneByOne(index + 1, selectedUrls)
        });
    }catch(err){
        alert('Failed with network!');
        originButton();
        return;
    }
}

const clearButton = document.getElementById('clearTerminal');

clearButton.onclick = () => {
    clearLogs();
}


const selectAll = document.getElementById("selectAll");

selectAll.addEventListener("change", () => {
    const checkboxes = document.querySelectorAll('input[name="urlcheckbox"]');
    if (selectAll.checked) {
        checkboxes.forEach((checkbox) => {
            checkbox.checked = true; // Disable each checkbox
        });
        addlog(checkboxes.length + ' websites are selected');
    } else {
        checkboxes.forEach((checkbox) => {
            checkbox.checked = false; // Disable each checkbox
        });
        addlog('No websites are selected');
    }
})

function handleSelected(self) {
    const url = self.getAttribute('data-url');
    if(!self.checked){
        addlog('➖ ' + url + ' released');
        return;
    }
    addlog('➕ ' + url + ' selected');
}