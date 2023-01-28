/* MOBILE PURPOSE */
function copyMenu() {
    var dptCategory = document.querySelector(".dpt-cat");
    var dptPlace = document.querySelector(".departments");

    dptPlace.innerHTML = dptCategory.innerHTML;


    var mainNav = document.querySelector(".header-nav nav");
    var navPlace = document.querySelector(".off-canvas nav");

    navPlace.innerHTML = mainNav.innerHTML;


    var topNav = document.querySelector(".header-top .wrapper");

    var topPlace = document.querySelector('.off-canvas .thetop-nav');

    topPlace.innerHTML = topNav.innerHTML;
}

copyMenu();



// Menu hamburger
const menuButton = document.querySelector('.trigger'),
    closeButton = document.querySelector('.t-close'),
    addclass = document.querySelector('.site');


menuButton.addEventListener('click', function() {
    addclass.classList.toggle('showmenu')
})

closeButton.addEventListener('click', function() {
    addclass.classList.remove('showmenu')
})






/* SHOW SUB MENU ON MOBILE DEVICE */

const submenu = document.querySelectorAll(".has-child .icon-small");

submenu.forEach((menu) => menu.addEventListener('click', toggle));

function toggle(e) {
    e.preventDefault();
    submenu.forEach((item) => item != this ? item.closest('.has-child').classList.remove('expand') : null);

    if (this.closest('.has-child').classList != 'expand') {
        this.closest('.has-child').classList.toggle('expand')
    }
}


submenu.forEach((menu) => menu.addEventListener('click', toggle));

function toggle(e) {
    e.preventDefault();
    submenu.forEach((item) => item != this ? item.closest('.has-child').classList.remove('expand') : null);

    if (this.closest('.has-child').classList != 'expand') {
        this.closest('.has-child').classList.toggle('expand')
    }
}


const swiper = new Swiper('.swiper', {
    // Optional parameters
    // direction: 'vertical',
    loop: true,

    // If we need pagination
    pagination: {
        el: '.swiper-pagination',
    },

    // Navigation arrows
    // navigation: {
    //     nextEl: '.swiper-button-next',
    //     prevEl: '.swiper-button-prev',
    // },

    // And if we need scrollbar
    // scrollbar: {
    //     el: '.swiper-scrollbar',
    // },
});

// SHOW MOBILE SEARCH FORM
const searchButton = document.querySelector('.t-search'),
    tClose = document.querySelector('.search-close'),
    showClass = document.querySelector('.site');


searchButton.addEventListener('click', function() {
    showClass.classList.toggle('showsearch')
})

tClose.addEventListener('click', function() {
    showClass.classList.remove('showsearch')
})

// SHOW CATEGORIE IN SINGLE PAGE

const dptButton = document.querySelector('.dpt-cat .dpt-trigger'),
    dptClass = document.querySelector('.site');

dptButton.addEventListener('click', function() {
    dptClass.classList.toggle('showdpt');
})

// SINGLE PAGE CAROUSEL

var productThumb = new Swiper('.small-image', {
    loop: true,
    spaceBetween: 10,
    slidesPerView: 3,
    freeMode: true,
    watchSlidesProgress: true,
    breakpoints: {
        481: {
            spaceBetween: 32,
        }
    }
})

var productBig = new Swiper('.big-image', {
    loop: true,
    autoHeight: true,
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
    thumbs: {
        swiper: productThumb
    }

})


const divtoShow = '.mini-cart';
const divPopup = document.querySelector(divtoShow);
const divTrigger = document.querySelector('.cart-trigger');

divTrigger.addEventListener('click', () => {
    setTimeout(() => {
        if (!divPopup.classList.contains('show')) {
            divPopup.classList.add('show');
        }
    }, 250)
})

document.addEventListener('click', (e) => {
    const isClosest = e.target.closest(divtoShow);

    if (!isClosest && divPopup.classList.contains('show')) {
        divPopup.classList.remove('show')
    }
})