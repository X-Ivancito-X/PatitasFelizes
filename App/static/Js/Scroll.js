window.addEventListener("scroll", () => {
    const header = document.getElementById("header");
    
    if (window.scrollY > 200) {
        header.classList.add("Arriba");

    } 
    else {
        header.classList.remove("Arriba");

    }
});
