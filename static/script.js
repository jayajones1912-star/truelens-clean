function toggleInfo(btn) {
    const extra = btn.nextElementSibling;

    if (extra.classList.contains("hidden")) {
        extra.classList.remove("hidden");
        btn.innerText = "Hide Info";
    } else {
        extra.classList.add("hidden");
        btn.innerText = "More Info";
    }
}
