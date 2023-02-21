const navSlide = () => {
    let nav = document.querySelector('nav')
    let dropdown = nav.querySelector('.dropdown')
    let dropdownToggle = nav.querySelector("[data-action='dropdown-toggle']")
    let navToggle = nav.querySelector("[data-action='nav-toggle']")
  
    window.addEventListener('scroll', ()=>{
      if(window.scrollY > 10){
        nav.classList.add('active_nav')
      } else{
        nav.classList.remove('active_nav')
      }
    })
  
    dropdownToggle.addEventListener('click', ()=>{
      if(dropdown.classList.contains('show')){
        dropdown.classList.remove('show')
      } else {
        dropdown.classList.add('show')
      }
    })
  
    navToggle.addEventListener('click', ()=>{
      if(nav.classList.contains('opened')){
        nav.classList.remove('opened')
      } else {
        nav.classList.add('opened')
      }
    })
  
}
navSlide();



function togglegrade(){
  const blur = document.querySelectorAll('.blur');
  for(let i=0;i<blur.length;i++){
    blur[i].classList.toggle('active')
  }
  const popupGrade = document.getElementById('popupgrade');
  popupGrade.classList.toggle('active')
}
function togglecontact(){
  const blur = document.querySelectorAll('.blur');
  for(let i=0;i<blur.length;i++){
    blur[i].classList.toggle('active')
  }
  const popupcontact = document.getElementById('popupcontact');
  popupcontact.classList.toggle('active')
}


function toggleexp(){
  var blur = document.querySelectorAll('.blur');
  for(let i=0;i<blur.length;i++){
    blur[i].classList.toggle('active')
  }
  var popupexperience = document.getElementById('popupexperience');
  popupexperience.classList.toggle('active')
}
function toggleexpEdit(){
  var blur = document.querySelectorAll('.blur');
  for(let i=0;i<blur.length;i++){
    blur[i].classList.toggle('active')
  }
  var popupexperience = document.getElementById('popupexperienceEdit');
  popupexperience.classList.toggle('active')
}
function editExperience(expid, userid){
  var blur = document.querySelectorAll('.blur');
  for(let i=0;i<blur.length;i++){
    blur[i].classList.toggle('active')
  }
  var popupexperience = document.getElementById('popupexperienceEdit');
  popupexperience.classList.toggle('active')

  document.getElementById('position_edit').value = document.getElementById('experience_title_'+expid+'').innerHTML

  let txt = document.getElementById('experience_company_'+expid+'').innerHTML
  let t = txt.split(':')
  document.getElementById('company_edit').value = t[0]

  let x = t[1].split('/')
  let r = []
  for(let k=0;k<x.length;k++){
    let w = x[k].replace(" ", "")
    w = x[k].trim()
    r.push(w)
  }
  console.log(r)
  document.getElementById('startexp_edit').value = r[0]
  document.getElementById('finishexp_edit').value = r[1]

  document.getElementById('description_edit').value = document.getElementById('experience_description_'+expid+'').innerHTML
}
function deleteExperience(expid, userid){
  fetch('/delete_added_experience/'+userid, {
    method: "POST",
    body: JSON.stringify({id: expid})
  }).then((_res) => {
    window.location.href = '/profilCV/'+userid
  })
}


function toggleabout(){
  var blur = document.querySelectorAll('.blur');
  for(let i=0;i<blur.length;i++){
    blur[i].classList.toggle('active')
  }
  var popupaboutme = document.getElementById('popupaboutme');
  popupaboutme.classList.toggle('active')
}


function toggleskills(){
  var blur = document.querySelectorAll('.blur');
  for(let i=0;i<blur.length;i++){
    blur[i].classList.toggle('active')
  }
  var popupskills = document.getElementById('popupskills');
  popupskills.classList.toggle('active')
}
function deleteSkills(skillid, userid){
  fetch('/delete_added_skills/'+userid, {
    method: "POST",
    body: JSON.stringify({id: skillid})
  }).then((_res) => {
    window.location.href = '/profilCV/'+userid
  })
}


function togglelang(){
  var blur = document.querySelectorAll('.blur');
  for(let i=0;i<blur.length;i++){
    blur[i].classList.toggle('active')
  }
  var popupslang = document.getElementById('popupslang');
  popupslang.classList.toggle('active')
}
function deleteLanguage(langid, userid){
  fetch('/delete_added_language/'+userid, {
    method: "POST",
    body: JSON.stringify({id: langid})
  }).then((_res) => {
    window.location.href = '/profilCV/'+userid
  })
}


function toggleedu(){
  var blur = document.querySelectorAll('.blur');
  for(let i=0;i<blur.length;i++){
    blur[i].classList.toggle('active')
  }
  var popupeducation = document.getElementById('popupeducation');
  popupeducation.classList.toggle('active')
}
function toggleeduEdit(){
  var blur = document.querySelectorAll('.blur');
  for(let i=0;i<blur.length;i++){
    blur[i].classList.toggle('active')
  }
  var popupeducation = document.getElementById('popupeducationEdit');
  popupeducation.classList.toggle('active')
}
function editEducation(expid, userid){
  var blur = document.querySelectorAll('.blur');
  for(let i=0;i<blur.length;i++){
    blur[i].classList.toggle('active')
  }
  var popupexperience = document.getElementById('popupeducationEdit');
  popupexperience.classList.toggle('active')

  document.getElementById('geteduID').value = document.getElementById('eduID').innerHTML

  document.getElementById('institution_edit').value = document.getElementById('education_studies_'+expid+'').innerHTML
  document.getElementById('specialization_edit').value = document.getElementById('education_title_'+expid+'').innerHTML
  let txt = document.getElementById('education_year_'+expid+'').innerHTML
  let t = txt.split('/')
  let r = []
  for(let k=0;k<t.length;k++){
    let w = t[k].replace(" ", "")
    w = t[k].trim()
    r.push(w)
  }
  document.getElementById('startyear_edit').value = r[0]
  const gradyear = document.querySelector('#graduationyear_edit')
    const ongoing = document.querySelector('#edu_ongoing_edit')
  if(r[1].toString() === 'ongoing'){
    gradyear.disabled = true;
    ongoing.checked = true;
    document.querySelector('#graduationyear_edit').value = ""
  } else{
    gradyear.disabled = false;
    ongoing.checked = false;
    document.querySelector('#graduationyear_edit').value = r[1]
  }


}
function deleteEducation(eduid, userid){
  fetch('/delete_added_ecucation/'+userid, {
    method: "POST",
    body: JSON.stringify({id: eduid})
  }).then((_res) => {
    window.location.href = '/profilCV/'+userid
  })
}


function togglehobbies(){
  var blur = document.querySelectorAll('.blur');
  for(let i=0;i<blur.length;i++){
    blur[i].classList.toggle('active')
  }
  var popuphobbies = document.getElementById('popuphobbies');
  popuphobbies.classList.toggle('active')
}
function deleteHobbies(hobbieid, userid){
  fetch('/delete_added_hobbies/'+userid, {
    method: "POST",
    body: JSON.stringify({id: hobbieid})
  }).then((_res) => {
    window.location.href = '/profilCV/'+userid
  })
}


function updateEdu(eduid, userid){
  fetch('/update_grade/'+userid, {
    method: "POST",
    body: JSON.stringify({id: eduid})
  }).then((_res) => {
    window.location.href = '/profilCV/'+userid
  })
}


function defaultBtnActive(){
  const defaultbtn = document.querySelector("#default-btn");
  const photo = document.querySelector("#addphoto");
  const img = document.querySelector("#selectedPhoto");
  defaultbtn.click()
}