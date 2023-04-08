const inputFile = document.getElementById('id_avatar_author')
const previewImageAvatar = document.querySelector('.current-avatar-profile')
if (previewImageAvatar) {
        var initialImage = previewImageAvatar.src
}


function deleteCurrentPhoto() {
    document.querySelector('input[type=file]').value = ''
    let blockInp = document.querySelector('.input-file-list')
    blockInp.style.display = 'none'
    previewImageAvatar.setAttribute('src', initialImage)
}

if (inputFile) {
    inputFile.addEventListener('change', function () {
        const file = this.files[0];

        let allowedExtensions =
            /(\.jpg|\.jpeg|\.png)$/i;

        let filePath = inputFile.value;


        if (!allowedExtensions.exec(filePath)) {
            alert('Допускается изображение только в формате jpg')
            inputFile.value = '';
            return false;
        } else {
            const reader = new FileReader();


            reader.onload = function () {
                if (previewImageAvatar) {
                    previewImageAvatar.setAttribute('src', reader.result)
                }
            }

            reader.readAsDataURL(file);
        }

        let blockInp = document.querySelector('.input-file-list')
        blockInp.style.display = 'flex'
        blockInp.style.flexDirection = 'row'
        blockInp.style.alignItems = 'center'
        blockInp.style.justifyContent = 'center'
        let name_file = document.querySelector('.input-file-list .name-file')
        name_file.innerHTML = inputFile.value.replace(/^.*[\\\/]/, '')
    })
}
