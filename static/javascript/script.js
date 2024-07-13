



const copyBtns = [...document.getElementsByClassName('copy_btn')]

console.log(copyBtns)

let previous = null

copyBtns.forEach(btn=> btn.addEventListener('click', ()=> {
	console.log('click')
	const short_url = btn.getAttribute('copy_content')
	navigator.clipboard.writeText(short_url)

	
}))