// Task Status Update Handler
function handleTaskStatusUpdate(taskId, newStatus, button) {
    // Get CSRF token from meta tag
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    
    // Disable button while processing
    button.disabled = true;
    
    const formData = new FormData();
    formData.append('status', newStatus);
    
    fetch(`/api/task-status-update/${taskId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            showToast('success', `Task status updated to ${data.new_status}`);
            // Reload the page after a short delay
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        } else {
            throw new Error(data.message || 'Failed to update task status');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('error', error.message || 'Failed to update task status. Please try again.');
        // Re-enable button
        button.disabled = false;
    });
}

// Toast Notification Handler
function showToast(type, message) {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type === 'error' ? 'danger' : 'success'} position-fixed top-0 end-0 m-3`;
    toast.style.zIndex = '1050';
    toast.textContent = message;
    document.body.appendChild(toast);
    
    // Remove toast after 3 seconds
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Workspace Member Update Handler
function updateWorkspaceMembers(workspaceId) {
    const assignedToSelect = document.getElementById('id_assigned_to');
    if (!assignedToSelect) return;

    fetch(`/api/workspace-members/${workspaceId}/`)
        .then(response => response.json())
        .then(data => {
            // Clear current options
            assignedToSelect.innerHTML = '';
            
            // Add new options
            data.members.forEach(member => {
                const option = new Option(member.username, member.id);
                assignedToSelect.add(option);
            });
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('error', 'Failed to update member list. Please try again.');
        });
}

// Initialize Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Task Status Buttons
    const statusButtons = document.querySelectorAll('.task-status-btn');
    statusButtons.forEach(button => {
        button.addEventListener('click', function() {
            handleTaskStatusUpdate(
                this.dataset.taskId,
                this.dataset.status,
                this
            );
        });
    });

    // Workspace Select in Task Form
    const workspaceSelect = document.getElementById('id_workspace');
    if (workspaceSelect) {
        workspaceSelect.addEventListener('change', function() {
            if (this.value) {
                updateWorkspaceMembers(this.value);
            }
        });
    }

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});
