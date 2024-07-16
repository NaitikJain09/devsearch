let form = document.getElementById("searchForm");
let pageLinks = document.getElementsByClassName("page--link");
if (form) {
	for (let i = 0; pageLinks.length > i; i++) {
		pageLinks[i].addEventListener("click", function(e) {
			e.preventDefault();
			let page = this.dataset.page;
			form.innerHTML += `<input value=${page} name="page" hidden>`;
			form.submit();
		});
	}
}
