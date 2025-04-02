// dynamic-menu.js - Implements interactive menu behaviors and navigation features
// This file handles the side menu, user authentication state, and dynamic UI updates

document.addEventListener('DOMContentLoaded', function () {
    console.log("Initializing dynamic UI components");

    // Get reference to website title element for toggling visibility
    const websiteTitle = document.querySelector('.logo h1');

    // ## SIDE MENU FUNCTIONALITY ##
    // This section creates an interactive slide-out menu
    const menuToggle = document.querySelector('.menu-toggle');
    const sideMenu = document.querySelector('.side-menu');
    const menuOverlay = document.querySelector('.menu-overlay');
    const closeMenu = document.querySelector('.close-menu');

    // Toggle menu visibility and handle page scrolling
    // This function handles the menu appearance based on user interaction
    function toggleMenu() {
        // Toggle active class to show/hide menu
        sideMenu.classList.toggle('active');
        menuOverlay.classList.toggle('active');

        // Disable page scrolling when menu is open to improve usability
        document.body.style.overflow = sideMenu.classList.contains('active') ? 'hidden' : '';
    }

    // Add event listeners for opening/closing the menu
    if (menuToggle) menuToggle.addEventListener('click', toggleMenu);
    if (closeMenu) closeMenu.addEventListener('click', toggleMenu);
    if (menuOverlay) menuOverlay.addEventListener('click', toggleMenu);

    // ## MENU CLICK OUTSIDE HANDLER ##
    // Close menu when clicking outside the menu area
    document.addEventListener('click', function (e) {
        if (sideMenu && menuToggle &&
            sideMenu.classList.contains('active') &&
            !sideMenu.contains(e.target) &&
            !menuToggle.contains(e.target)) {

            // Hide menu and overlay
            sideMenu.classList.remove('active');
            if (menuOverlay) menuOverlay.classList.remove('active');

            // Re-enable page scrolling
            document.body.style.overflow = '';
        }
    });


    // ## MENU ITEM ANIMATIONS ##
    // Animated entrance for menu items when opening side menu
    const menuLinks = document.querySelectorAll('.menu-section a');

    // Set initial state for menu items - invisible and shifted left
    menuLinks.forEach((link, index) => {
        link.style.opacity = '0';
        link.style.transform = 'translateX(-20px)';

        // Stagger the animation timing for a cascade effect
        link.style.transition = `all 0.1s ease ${index * 0.02}s`;
    });

    // Animate menu items when menu finishes opening
    if (sideMenu) {
        sideMenu.addEventListener('transitionend', function (e) {
            if (e.propertyName === 'left' && sideMenu.classList.contains('active')) {
                // Make each link visible and move to original position
                menuLinks.forEach(link => {
                    link.style.opacity = '1';
                    link.style.transform = 'translateX(0)';
                });
            }
        });
    }

    // ## NAVBAR SCROLL BEHAVIOR ##
    // Smart navbar that hides when scrolling down and reappears when scrolling up
    let lastScrollTop = 0;
    const navbar = document.querySelector('.navbar');

    if (navbar) {
        // Listen for scroll events to toggle navbar visibility
        window.addEventListener('scroll', function () {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

            // Hide navbar when scrolling down (past 100px threshold)
            if (scrollTop > lastScrollTop && scrollTop > 100) {
                navbar.style.transform = 'translateY(-100%)'; // Slide up out of view
            } else {
                // Show navbar when scrolling up
                navbar.style.transform = 'translateY(0)'; // Slide back into view
            }

            // Update last scroll position
            lastScrollTop = scrollTop;
        });
    }

    // ## ACTIVE PAGE HIGHLIGHTING ##
    // Highlight the current page in navigation menus
    // This improves user experience by showing current location
    function setActivePageInMenus() {
        // Get current page filename from URL
        const currentPath = window.location.pathname;
        const pageName = currentPath.split('/').pop();

        // Highlight matching link in side menu if it exists
        const sideMenuLinks = document.querySelectorAll('.side-menu a');
        sideMenuLinks.forEach(link => {
            if (link.getAttribute('href') === pageName) {
                link.style.backgroundColor = 'rgba(151, 4, 33, 0.1)';
                link.style.color = '#970421';
                link.style.fontWeight = 'bold';
            }
        });

        // Highlight matching link in top nav menu
        const navLinks = document.querySelectorAll('.nav-links a');
        navLinks.forEach(link => {
            if (link.getAttribute('href') === pageName) {
                link.style.color = '#970421';
                link.style.fontWeight = 'bold';
            }
        });
    }

    // ## UPDATE UI ELEMENTS BASED ON USER ROLE AND LOGIN STATUS ##
    // This keeps the interface consistent with authentication state
    function updateUIBasedOnUserRole() {
        // Check if user is logged in
        const isLoggedIn = sessionStorage.getItem('userLoggedIn') === 'true';
        const userRole = sessionStorage.getItem('userRole');

        console.log("UI update - User logged in:", isLoggedIn, "Role:", userRole);

        // Find UI elements to toggle
        const loginButtons = document.querySelectorAll('.login-btn');
        const profileDropdowns = document.querySelectorAll('.profile-dropdown');
        const managerOnlyElements = document.querySelectorAll('.manager-only');
        const technicianOnlyElements = document.querySelectorAll('.technician-only');
        const repairOnlyElements = document.querySelectorAll('.repair-only');

        if (isLoggedIn) {
            // User is logged in - show profile dropdown, hide login button
            loginButtons.forEach(btn => {
                btn.style.display = 'none';
            });

            profileDropdowns.forEach(dropdown => {
                dropdown.style.display = 'inline-block';
            });

            // Update profile initials using stored name
            const userName = sessionStorage.getItem('userName');
            if (userName) {
                const nameParts = userName.split(' ');
                let initials = nameParts[0].charAt(0).toUpperCase();

                if (nameParts.length > 1) {
                    initials += nameParts[1].charAt(0).toUpperCase();
                }

                const profileIcons = document.querySelectorAll('.profile-icon');
                profileIcons.forEach(icon => {
                    if (icon) {
                        icon.textContent = initials;
                    }
                });
            }


            // Show/hide elements based on user role
            if (userRole === 'manager') {
                managerOnlyElements.forEach(el => el.style.display = '');
                technicianOnlyElements.forEach(el => el.style.display = 'none');
                repairOnlyElements.forEach(el => el.style.display = 'none');
            } else if (userRole === 'technician') {
                managerOnlyElements.forEach(el => el.style.display = 'none');
                technicianOnlyElements.forEach(el => el.style.display = '');
                repairOnlyElements.forEach(el => el.style.display = 'none');
            } else if (userRole === 'repair') {
                managerOnlyElements.forEach(el => el.style.display = 'none');
                technicianOnlyElements.forEach(el => el.style.display = 'none');
                repairOnlyElements.forEach(el => el.style.display = '');
            }
        } else {
            // User is not logged in - hide profile dropdown, show login button
            loginButtons.forEach(btn => {
                btn.style.display = 'inline-block';
            });

            profileDropdowns.forEach(dropdown => {
                dropdown.style.display = 'none';
            });

            // Hide role-specific elements when not logged in
            managerOnlyElements.forEach(el => el.style.display = 'none');
            technicianOnlyElements.forEach(el => el.style.display = 'none');
            repairOnlyElements.forEach(el => el.style.display = 'none');
        }
    }

    // ## HANDLE TAB SWITCHING ##
    // For pages with tabbed interfaces
    function initializeTabs() {
        const tabs = document.querySelectorAll('.tab');
        const tabContents = document.querySelectorAll('.tab-content');

        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                // Remove active class from all tabs
                tabs.forEach(t => t.classList.remove('active'));
                tabContents.forEach(c => c.classList.remove('active'));

                // Add active class to clicked tab
                tab.classList.add('active');
                const tabContentId = tab.getAttribute('data-tab');
                const content = document.getElementById(tabContentId);
                if (content) {
                    content.classList.add('active');
                }
            });
        });
    }

    // ## STYLE COLLECTION CHECKBOXES ##
    // Apply styling to collection checkboxes in edit machine page
    function styleCollectionCheckboxes() {
        const collectionCheckboxes = document.querySelectorAll('.collection-checkbox');

        collectionCheckboxes.forEach(checkbox => {
            const input = checkbox.querySelector('input');

            // Set initial state
            if (input && input.checked) {
                checkbox.style.backgroundColor = 'rgba(151, 4, 33, 0.05)';
                checkbox.style.borderColor = '#970421';
            }

            // Add change handler
            if (input) {
                input.addEventListener('change', function () {
                    if (this.checked) {
                        checkbox.style.backgroundColor = 'rgba(151, 4, 33, 0.05)';
                        checkbox.style.borderColor = '#970421';
                    } else {
                        checkbox.style.backgroundColor = 'white';
                        checkbox.style.borderColor = 'var(--border-color)';
                    }
                });
            }
        });
    }

    // ## LOGOUT FUNCTIONALITY ##
    // Attach event listeners to logout links
    function setupLogoutHandlers() {
        const logoutLinks = document.querySelectorAll('.logout-link');

        logoutLinks.forEach(link => {
            link.addEventListener('click', function (e) {
                // Only do this special handling if we're logged in
                if (sessionStorage.getItem('userLoggedIn') === 'true') {
                    e.preventDefault();

                    // Clear session storage
                    sessionStorage.removeItem('userLoggedIn');
                    sessionStorage.removeItem('userName');
                    sessionStorage.removeItem('userRole');

                    // Redirect to login page
                    window.location.href = 'login.html';
                }
            });
        });
    }

    // Call initialization functions when DOM loads
    setActivePageInMenus();
    updateUIBasedOnUserRole();
    initializeTabs();
    styleCollectionCheckboxes();
    setupLogoutHandlers();

});