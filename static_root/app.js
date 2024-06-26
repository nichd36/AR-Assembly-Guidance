const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        console.log(entry)
        if (entry.isIntersecting){
            entry.target.classList.add('show');
        } else {
            entry.target.classList.remove('show');
        }
    });
});

console.log("Script Loaded");

const periksa = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        console.log(entry)
        if (entry.isIntersecting){
            entry.target.classList.add('show');
        }
    });
});

const upcomingObject = document.querySelectorAll('.upcoming,.fog,.upcominggg');
upcomingObject.forEach((el) => observer.observe(el));

const onceObject = document.querySelectorAll('.upcoming-once,.upcomingX');
onceObject.forEach((el) => periksa.observe(el));

window.onscroll = function() {myFunction()};

var header = document.getElementById("myHeader");
var sticky = document.getElementById("sticky");
var active = document.getElementById("active");
var subMenu = document.getElementById("subMenu");
var hamburger = document.getElementById("hamburger-menu");
var sticky = header.offsetTop;

function myFunction() {
  if (window.pageYOffset > sticky) {
    header.classList.add("sticky");
    header.classList.add("active");
  } else {
    header.classList.remove("sticky");
    header.classList.remove("active");
  }
}

let processScroll = () => {
    let docElem = document.documentElement, 
        docBody = document.body,
        scrollTop = docElem['scrollTop'] || docBody['scrollTop'],
        scrollBottom = (docElem['scrollHeight'] || docBody['scrollHeight']) - window.innerHeight,
        scrollPercent = scrollTop / scrollBottom * 100 + '%';
    
    // console.log(scrollTop + ' / ' + scrollBottom + ' / ' + scrollPercent);
    
    document.getElementById("progress-bar").style.setProperty("--scrollAmount", scrollPercent); 
}

document.addEventListener('scroll', processScroll);

function toggleMenu(){
    subMenu.classList.toggle("open-menu");
    hamburger.classList.toggle("background");

    // Get the current source of the hamburger image
    var currentSrc = hamburger.src;
    console.log("CurrentSrc:", currentSrc);
    console.log("LightMenuUrl:", lightMenuUrl);
    console.log("CloseLightMenuUrl:", closeLightMenuUrl);

    // Check if the current source contains 'light_menu.png'
    if (currentSrc.includes(closeLightMenuUrl)) {
        hamburger.src = lightMenuUrl;
    } else {
        // Otherwise, replace it with 'light_menu.png'
        hamburger.src = closeLightMenuUrl;
    }
}


function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}
  
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}


// const userThemePreference = localStorage.getItem('theme');
// if (userThemePreference === 'dark') {
//     document.body.style.transition = 'none';
//     document.body.classList.add('dark-mode');
//     setTimeout(() => {
//         document.body.style.transition = '';
//     }, 0);
//   }

const themeToggle = document.getElementById('theme-toggle');

function toggleDarkTheme() {
  document.body.classList.toggle('dark-mode');
  console.log("Dark mode toggled")
  const currentTheme = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
  console.log(currentTheme)
  localStorage.setItem('theme', currentTheme);
}

themeToggle.addEventListener('click', toggleDarkTheme);

function openPopUp(i) {
    document.getElementById("popup-box"+i).style.display = "block";
  }
  
  function closePopUp(i) {
    document.getElementById("popup-box"+i).style.display = "none";
  }