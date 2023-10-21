window.showToast = function(message, type) {
    const toastContainer = document.getElementById('toastContainer');

    // Create the toast element
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;

    // Append the toast to the container
    toastContainer.appendChild(toast);

    // Show the toast with animation
    setTimeout(() => {
        toast.classList.add('show-toast');
        toast.classList.add(type);
    }, 100);

    // Remove the toast after a certain duration
    setTimeout(() => {
        toast.classList.remove('show-toast');
        setTimeout(() => {
            toastContainer.removeChild(toast);
        }, 300);
    }, 3000);
}