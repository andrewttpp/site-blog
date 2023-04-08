document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('burger').addEventListener('click', function () {
        document.querySelector('header').classList.toggle('open')
    })

    if (document.getElementById('name_user')) {
        document.getElementById('name_user').addEventListener('click', function () {
            document.querySelector('.menu_user').classList.toggle('menu_user_open')
            let triangles = document.getElementById('label-categories-triangle-burger')
            if (document.querySelector('.menu_user').classList.contains('menu_user_open')) {
                triangles.style.borderTop = 'none'
                triangles.style.borderBottom = '6px solid #fdc073'
            } else {
                triangles.style.borderBottom = 'none'
                triangles.style.borderTop = '6px solid #fdc073'
            }
        })
    }

    let articlesRelative = document.querySelector('.title-public-articles-relative')
    if (document.getElementById('title-public-articles-triangle')) {
        articlesRelative.style.display = 'block'
        document.querySelector('.title-public-articles-relative').addEventListener('click', function () {
            document.querySelector('.title-public-articles-relative').classList.toggle('articles-open')
            let triangles = document.getElementById('title-public-articles-triangle')
            let articles = document.querySelector('.articles-user')
            if (document.querySelector('.title-public-articles-relative').classList.contains('articles-open')) {
                triangles.style.borderTop = 'none'
                triangles.style.borderBottom = '6px solid black'
                articles.style.display = 'block'
            } else {
                triangles.style.borderBottom = 'none'
                triangles.style.borderTop = '6px solid black'
                articles.style.display = 'none'
            }
        })
    } else {
        if (articlesRelative) {
            articlesRelative.style.display = 'flex'
            articlesRelative.style.flexDirection = 'column'
        }
    }

    let articlesUser = document.querySelector('.articles-user')
    if (articlesUser) {
        document.querySelector('.main').style.flexDirection = 'column'
    }


    document.getElementById('title-categories').addEventListener('click', function () {
        document.querySelector('#menu_categories').classList.toggle('open')
        let triangles = document.querySelector('#burger-categories #label-categories-triangle-burger')
        if (document.querySelector('#menu_categories').classList.contains('open')) {
            triangles.style.borderTop = 'none'
            triangles.style.borderBottom = '6px solid #fdc073'
        } else {
            triangles.style.borderBottom = 'none'
            triangles.style.borderTop = '6px solid #fdc073'
        }
    })

    let menu_user = document.querySelector('.menu_user_header')
    document.querySelector('.user-button_header').addEventListener('click', function () {
        menu_user.classList.add('open-menu-user-header')
    })


    document.onclick = function (e) {
        if (e.target.className !== "user-button_header") {
            menu_user.classList.remove('open-menu-user-header')
        }
    };

    if (document.querySelector('.my-profile-form')) {
        document.querySelector('.main').style.flexDirection = 'column';
        if (document.querySelector('.success') || document.querySelector('.error')) {
            document.querySelector('.form').style.marginTop = '0';
        }

        console.log(document.querySelector('.name-file').style.width)
    }

    if (document.querySelector('.change-password')) {
        document.querySelector('.main').style.flexDirection = 'column'
    }
})

document.querySelector('.user-block_header').style = 'margin-left: 455px'

document.activeElement.blur();

let triangle = document.getElementById('label-categories-triangle')
let el = document.getElementsByClassName('categories-chapter');
for (let i = 0; i < el.length; i++) {
    el[i].addEventListener("mouseenter", showSub, false);
    el[i].addEventListener("mouseleave", hideSub, false);
}

function showSub(e) {
    if (this.children.length > 1) {
        this.children[1].style.height = "auto";
        this.children[1].style.overflow = "visible";
        this.children[1].style.opacity = "1";
        triangle.style.borderTop = 'none'
        triangle.style.borderBottom = '6px solid #1C1C1C'
    } else {
        return false;
    }
}

function hideSub(e) {
    if (this.children.length > 1) {
        this.children[1].style.height = "0px";
        this.children[1].style.overflow = "hidden";
        this.children[1].style.opacity = "0";
        triangle.style.borderBottom = 'none'
        triangle.style.borderTop = '6px solid #1C1C1C'
    } else {
        return false;
    }
}

let dateInput = document.querySelector('#id_date_birthday')
if (dateInput) {
    console.log(dateInput.value)
}

