// Borders
let normal = '0px solid black'
let highlight = '2px solid yellow'

// Get sections
let body = document.querySelector('body')
let array_section = document.querySelector('.array')
let img_cnt = array_section.childElementCount
let single_section = document.querySelector('.single')
let full_scr_img = single_section.firstElementChild

// Highlight first image
let img_index = 1
let el = document.querySelector(`img:nth-of-type(${img_index})`)
el.style.border = highlight

let full_scr = false

function toggleFullScreen() {
  if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen()
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen()
    }
  }
}

// Keyboard events
document.addEventListener('keydown', function(e) {
    if(e.key == 'Enter') {
	if(!full_scr) {
	    // Get the current image path
	    let el = document.querySelector(`img:nth-of-type(${img_index})`)
	    let thumb_path = el.getAttribute('src')
	    let master_path = thumb_path.replace('thumbnails', 'master')
	    full_scr_img.setAttribute('src', master_path)

	    body.style.overflow = 'hidden'
	    array_section.style.display = 'none'
	    single_section.style.display = 'block'
	    toggleFullScreen()
	    full_scr = true
	}
	return
    }
    
    // Left and right arrows move among images
    let arrows = ['ArrowUp', 'ArrowRight', 'ArrowDown', 'ArrowLeft']
    let n = arrows.indexOf(e.key)
    if(n == 0 || n == 2) {
	return
    }
    if(n == 1) {
	// Right
	// FIXME get the actual size
	if(img_index < img_cnt) {
	    img_index += 1
	}
    }
    else {
	// Left
	if(img_index > 1) {
	    img_index -= 1
	}
    }
    if(full_scr) {
	// Get the current image path
	let el = document.querySelector(`img:nth-of-type(${img_index})`)
	let thumb_path = el.getAttribute('src')
	let master_path = thumb_path.replace('thumbnails', 'master')
	full_scr_img.setAttribute('src', master_path)
    }
    else {
	// Update the border style
	el.style.border = normal
	el = document.querySelector(`img:nth-of-type(${img_index})`)
	el.style.border = highlight
    }
})

// Full screen events
document.addEventListener('fullscreenchange', function(e) {
    if(!document.fullscreenElement) {
	// Leaving full screen mode
	body.style.overflow = 'auto'
	array_section.style.display = 'block'
	single_section.style.display = 'none'

	el.style.border = normal
	el = document.querySelector(`img:nth-of-type(${img_index})`)
	el.style.border = highlight
	full_scr = false
    }
})
