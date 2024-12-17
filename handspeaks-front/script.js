const menuToggle = document.querySelector('.menu-toggle');
const navigation = document.querySelector('.navigation');

menuToggle.addEventListener('click', () => {
    navigation.classList.toggle('active');
});
// JavaScript to handle the active link highlight and background movement
const navLinks = document.querySelectorAll('.navigation li a');

// Initially set the active state for the current page link
window.addEventListener('DOMContentLoaded', () => {
    const currentUrl = window.location.pathname;
    navLinks.forEach((link) => {
        if (link.href.includes(currentUrl)) {
            link.classList.add('active');
        }
    });
});

// Add active class and move the background highlight based on clicks
navLinks.forEach((link) => {
    link.addEventListener('click', (e) => {
        navLinks.forEach((nav) => nav.classList.remove('active'));
        e.currentTarget.classList.add('active');
    });
});

// JavaScript to dynamically change text in the hero section with delay
document.addEventListener('DOMContentLoaded', function() {
    let text1 = document.getElementById('dynamic-text1');
    let text2 = document.getElementById('dynamic-text2');
    let text3 = document.getElementById('dynamic-text3');

    // Set initial text
    text1.innerHTML = 'First Ever Thought of Hand Gesture Recognition Smart Watch';
    text2.innerHTML = 'This smartwatch aims to revolutionize the way we interact with technology, using gestures.';
    text3.innerHTML = 'Train and test the gesture recognition model for accuracy.';

    // Set initial opacity for all text elements (hidden initially)
    text1.style.opacity = 0;
    text2.style.opacity = 0;
    text3.style.opacity = 0;

    // Fade in the first text after 1 second
    setTimeout(function() {
        text1.style.opacity = 1; // Fade in the first text
    }, 1000); 

    // Fade in the second text after 6 seconds (making the first text visible for a longer time)
    setTimeout(function() {
        text2.style.opacity = 1; // Fade in the second text
    }, 6000); 

    // Fade in the third text after 11 seconds (making the second text visible for a while)
    setTimeout(function() {
        text3.style.opacity = 1; // Fade in the third text
    }, 11000);

    // Change text content after specific time delays
    setTimeout(function() {
        text1.innerHTML = 'TEST AND TRAIN THE MODEL';
    }, 5000); // Change the first text after 5 seconds

    setTimeout(function() {
        text2.innerHTML = 'WATCH THE TUTORIALS';
        // You can add a link or button here to watch tutorials
    }, 10000); // Change the second text after 10 seconds
});
