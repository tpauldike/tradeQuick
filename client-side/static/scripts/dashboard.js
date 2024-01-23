function showConversation(username) {
    // Get the selected conversation section
    console.log('showConversation called with username:', username);
    var selectedSection = document.getElementById(username + 'Conversation');

    // Hide all conversation sections
    var allSections = document.querySelectorAll('aside > div');
    allSections.forEach(function (section) {
        if (section !== selectedSection) {
            section.style.display = 'none';
        }
    });

    // Toggle the visibility of the selected conversation section
    if (selectedSection) {
        if (selectedSection.style.display === 'block') {
            selectedSection.style.display = 'none';  // If visible, hide it
        } else {
            // If hidden or not set, show it
            selectedSection.style.display = 'block';
        }
    }
}


// JavaScript function to toggle the visibility of main elements
function toggleMain(mainId) {
        // Hide all main elements
        const allMainElements = document.querySelectorAll('main');
        allMainElements.forEach(function (main) {
            main.style.display = 'none';
        });

        // Show the selected main element
        const selectedMain = document.getElementById(mainId);
        if (selectedMain) {
            selectedMain.style.display = 'block';
        }
    }

    document.addEventListener('DOMContentLoaded', function() {
        var notificationButton = document.getElementById('notificationButton');
        var dropNot = document.getElementById('drop-not');
        
        var userButton = document.getElementById('userButton');
        var dropUser = document.getElementById('drop-user');
        
        // Add click event listener to the notification button
        notificationButton.addEventListener('click', function() {
            // Toggle visibility for drop-not
            dropNot.classList.toggle('visible');
            
            // If drop-user is visible, hide it
            if (dropUser.classList.contains('visible')) {
                dropUser.classList.remove('visible');
            }
        });
        
        // Add click event listener to the user button
        userButton.addEventListener('click', function() {
            // Toggle visibility for drop-user
            dropUser.classList.toggle('visible');
            
            // If drop-not is visible, hide it
            if (dropNot.classList.contains('visible')) {
                dropNot.classList.remove('visible');
            }
        });
    });



