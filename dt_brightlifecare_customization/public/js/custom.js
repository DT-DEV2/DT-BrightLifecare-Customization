if (window.location.href.includes("supplier")) {
    const buttons = document.querySelectorAll(".btn-google");
    buttons.forEach(btn => {
        btn.style.display = "none";
    });

}