function EnableDisable(ongoing){
    const gradyear = document.getElementById('graduationyear')
    gradyear.disabled = ongoing.checked;
}

function EnableDisableEdu(ongoing){
    const gradyea = document.getElementById('graduationyear_edit')
    gradyea.disabled = ongoing.checked;
}

function EnableDisableexp(ongoing){
    const gradyear = document.getElementById('finishexp')
    gradyear.disabled = ongoing.checked;
}


// SHOW MENU

const showMenu = (toggleId, navId) =>{
    const toggle = document.getElementById(toggleId),
    nav = document.getElementById(navId)

    // Validate that variables exist
    if(toggle && nav){
        toggle.addEventListener('click', ()=>{
            // We add the show-menu class to the div tag with the nav__menu class
            nav.classList.toggle('show-menu')
        })
    }
}
showMenu('nav-toggle','nav-menu')


// REMOVE MENU MOBILE

const navLink = document.querySelectorAll('.nav__link')

function linkAction(){
    const navMenu = document.getElementById('nav-menu')
    // When we click on each nav__link, we remove the show-menu class
    navMenu.classList.remove('show-menu')
}
navLink.forEach(n => n.addEventListener('click', linkAction))


// SCROLL SECTIONS ACTIVE LINK

const sections = document.querySelectorAll('section[id]')

function scrollActive(){
    const scrollY = window.pageYOffset

    sections.forEach(current =>{
        const sectionHeight = current.offsetHeight
        const sectionTop = current.offsetTop - 50;
        sectionId = current.getAttribute('id')

        if(scrollY > sectionTop && scrollY <= sectionTop + sectionHeight){
            document.querySelector('.nav__menu a[href*=' + sectionId + ']').classList.add('active-link')
        }else{
            document.querySelector('.nav__menu a[href*=' + sectionId + ']').classList.remove('active-link')
        }
    })
}
window.addEventListener('scroll', scrollActive)



/*==================== SHOW SCROLL TOP ====================*/
function scrollTop(){
    const scrollTop = document.getElementById('scroll-top');
    // When the scroll is higher than 560 viewport height, add the show-scroll class to the 'a' tag with the scroll-top class
    if(this.scrollY >= 560) scrollTop.classList.add('show-scroll'); else scrollTop.classList.remove('show-scroll')
}
window.addEventListener('scroll', scrollTop)


/*==================== DARK LIGHT THEME ====================*/ 
const themeButton = document.getElementById('theme-button')
const darkTheme = 'dark-theme'
const iconTheme = 'bx-sun'

// Previously selected topic (if user selected)
const selectedTheme = localStorage.getItem('selected-theme')
const selectedIcon = localStorage.getItem('selected-icon')

// We obtain the current theme that the interface has by validating the dark-theme class
const getCurrentTheme = () => document.getElementById('lmain').classList.contains(darkTheme) ? 'dark' : 'light'
const getCurrentIcon = () => themeButton.classList.contains(iconTheme) ? 'bx-moon' : 'bx-sun'

// We validate if the user previously chose a topic
if (selectedTheme) {
  // If the validation is fulfilled, we ask what the issue was to know if we activated or deactivated the dark
  document.getElementById('lmain').classList[selectedTheme === 'dark' ? 'add' : 'remove'](darkTheme)
  themeButton.classList[selectedIcon === 'bx-moon' ? 'add' : 'remove'](iconTheme)
}

// Activate / deactivate the theme manually with the button
themeButton.addEventListener('click', () => {
    // Add or remove the dark / icon theme
    document.getElementById('lmain').classList.toggle(darkTheme)
    themeButton.classList.toggle(iconTheme)
    // We save the theme and the current icon that the user chose
    localStorage.setItem('selected-theme', getCurrentTheme())
    localStorage.setItem('selected-icon', getCurrentIcon())
})



//  REDUCE THE SIZE AND PRINT ON A A4 SHEET
function scaleCV(){
    document.querySelector('.l-main').classList.add('scale-cv')
}


// REMOVE THE SIZE WHEM THE CV IS DOWNLOADED
function removeScale(){
    document.querySelector('.l-main').classList.remove('scale-cv')
}


// GENERATE PDF
let areaCV = document.getElementById('lmain')

let resumeButton = document.getElementById('resume-button')

// Html2pdf options
let studentname = document.getElementById('student_name')
let opt = {
    margin:       0,
    filename:     studentname.innerText + '.pdf',
    image:        { type: 'jpeg', quality: 1 },
    html2canvas:  { scale: 6 },
    jsPDF:        { format: 'a4', orientation: 'portrait' }
  };

// Function to call areaCV to Html2Pdf otpions
function generatedResume(){
    html2pdf(areaCV, opt)
}

// When the button is clicked, it executes three functions
resumeButton.addEventListener('click', () =>{
    // 1. The class .scale-cv is added to the class .l-main, where it reduces the size of the cv
    scaleCV()

    // 2. The PDF is generated
    generatedResume()

    // 3. The .scale-cv class is removed from the .l-main class to return to normal size
    setTimeout(removeScale, 1000)
})