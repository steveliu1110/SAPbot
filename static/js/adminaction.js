var flag = 0; // 'start', ''
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
        if (data.message) {
            alert(data.message);  // Show success message
            addWebsiteModal.classList.add('hidden');  // Close the modal

        } else {
            alert('Error: ' + data.error);  // Show error message
        }
    })
    .catch(error => {
        alert('There was an error submitting the form', error);
        print(error)
    });
});



const updateButton = document.getElementById('updateButton');
const scrapystate = document.getElementById('scrapystate');

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
        scrapystate.value += "⛔Stop scrapying...\n";
        return;
    }
    const checkboxes = document.querySelectorAll('input[name="urlcheckbox"]:checked'); 
    const selectedUrls = [];  
    checkboxes.forEach((checkbox) => {  
        selectedUrls.push(checkbox.getAttribute('data-url'));  
    }); 
    count = selectedUrls.length;
    if(count == 0){
        scrapystate.value += "⚠️ Pleas select the websites for updating\n";
        scrapystate.scrollTo(0,10000);
        return;
    }
    index = 0;
    flag = true;
    changeCheckbox(true);
    scrapystate.value += "🚀Start scrapying for selected websites...\n\n"
    scrapystate.scrollTo(0,10000);
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
        scrapystate.value += "🔚Completed updating!\n";
        scrapystate.scrollTo(0,10000);
        changeCheckbox(false);
        return;
    }
    scrapystate.value += "⚡Starting scrapying for 🌐" + selectedUrls[index] + "🌐\n";
    if(!flag){  
        scrapystate.value += "✋Scraping Stopped By User\n";
        scrapystate.scrollTo(0,10000);
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
                scrapystate.value += "Successfully completed scrapying for website 🌐" + data.result[0] + "🌐\n";
                scrapystate.value += "                Chunk Count is " + data.result[1] + "\n";
                scrapystate.value += "                Updated Date is " + data.result[2] + "\n";
                scrapystate.value += "\n";
                scrapystate.scrollTo(0,10000);
            }
            else{
                scrapystate.value += "Failed with scrapying for website " + selectedUrls[index] + "\n";
                scrapystate.value += "Error occured " + data.message+ "\n";
                scrapystate.value += "\n";
                scrapystate.scrollTo(0,10000);
            }
            updateOneByOne(index + 1, selectedUrls)
        })
        .catch(error => {
            scrapystate.value += "Successfully completed scrapying for website 🌐" + data.result[0] + "🌐\n";
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
    scrapystate.value = '';
}