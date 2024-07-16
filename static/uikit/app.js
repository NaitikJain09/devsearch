// Invoke Functions Call on Document Loaded
// document.addEventListener("DOMContentLoaded", function() {
// 	hljs.highlightAll();
// });

const close_alert = () => {
	alerts = document.getElementsByClassName("alert");
	for (let alert of alerts) {
		alert.style.display = "none";
	}
};
