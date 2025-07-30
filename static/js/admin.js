// Admin JavaScript Functions

let currentUserId = null;

function openPasswordModal(userId, username) {
    currentUserId = userId;
    document.getElementById('passwordModal').style.display = 'block';
    document.querySelector('.modal-header h3').textContent = `Change Password for ${username}`;
    document.getElementById('passwordForm').action = `/admin/change-password/${userId}`;
}

function closePasswordModal() {
    document.getElementById('passwordModal').style.display = 'none';
    document.getElementById('passwordForm').reset();
    currentUserId = null;
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('passwordModal');
    if (event.target === modal) {
        closePasswordModal();
    }
}

// Close modal with Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closePasswordModal();
    }
});

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Auto-remove flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });
}); 