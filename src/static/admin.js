const select_checkboxes = document.querySelectorAll('.select-item')
const selected_items_del = document.getElementById('selected-items-del')
const selected_items_act = document.getElementById('selected-items-act')

let SELECTED = []

function searchTable() {
  const input = document.getElementById('searchInput');
  const filter = input.value.toLowerCase();
  const table = document.getElementById('dataTable');
  const rows = table.getElementsByTagName('tr');

  for (let i = 1; i < rows.length; i++) {
      const cells = rows[i].getElementsByTagName('td');
      let match = false;

      for (let j = 0; j < cells.length; j++) {
          const originalText = cells[j].getAttribute('data-original-text') || cells[j].innerText;

          if (!cells[j].hasAttribute('data-original-text')) {
              cells[j].setAttribute('data-original-text', originalText);
          }

          cells[j].innerText = originalText;

          if (originalText.toLowerCase().includes(filter)) {
              match = true;

              const regex = new RegExp(`(${filter})`, 'gi');
              cells[j].innerHTML = originalText.replace(regex, '<span class="highlight-dashboard">$1</span>');
          }
      }

      rows[i].style.display = match ? '' : 'none';
  }
}

function trackSelected(arr) {
    console.log("CHECK" + arr)
    selected_track = document.getElementById("select-track")
    selected_track.textContent = arr.length
    selected_items_del.value = arr
    selected_items_act.value = arr
}

document.addEventListener("DOMContentLoaded", () => {
    select_checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            if (checkbox.checked) {
                SELECTED.push(checkbox.value)
                trackSelected(SELECTED)
            } else {
                SELECTED = SELECTED.filter(item => item !== checkbox.value)
                trackSelected(SELECTED)
            }
        })
    })
})

document.addEventListener("DOMContentLoaded", () => {
    select_all_checkboxes = document.querySelector('.select-all')
    
    select_all_checkboxes.addEventListener('change', () => {
        if (select_all_checkboxes.checked) {
            SELECTED = []
            select_checkboxes.forEach(checkbox => {
                checkbox.checked = true
                SELECTED.push(checkbox.value)
            })
            trackSelected(SELECTED)
        } else {
            select_checkboxes.forEach(checkbox => {
                checkbox.checked = false
            })
            SELECTED = []
            trackSelected(SELECTED)
        }
    })
})

document.getElementById("delete-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = document.getElementById("delete-form");
  
    const formData = new FormData(form);
    try {
        const response = await fetch(`/auth/admin/disable_user`, {
            method: 'POST',
            body: formData
        });
  
        if (response.redirected) {
            window.location.href = response.url;
        } else {
          const result = await response.json();
            alert(result.detail || "An error occurred during submission.");
        }
    } catch (error) {
        console.error("Submission failed:", error);
        alert("Failed to send data to the server.");
    }
  });

  document.getElementById("activate-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = document.getElementById("activate-form");
  
    const formData = new FormData(form);
    try {
        const response = await fetch(`/auth/admin/activate_user`, {
            method: 'POST',
            body: formData
        });
  
        if (response.redirected) {
            window.location.href = response.url;
        } else {
          const result = await response.json();
            alert(result.detail || "An error occurred during submission.");
        }
    } catch (error) {
        console.error("Submission failed:", error);
        alert("Failed to send data to the server.");
    }
  });

