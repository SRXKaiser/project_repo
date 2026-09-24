document.addEventListener("DOMContentLoaded", () => {

    // =====================================================
    // MENÚ RESPONSIVE
    // =====================================================

    const menuButton =
        document.querySelector(
            "[data-menu-button]"
        );

    const navigation =
        document.querySelector(
            "[data-navigation]"
        );

    if (menuButton && navigation) {

        menuButton.addEventListener(
            "click",
            () => {

                navigation.classList.toggle(
                    "is-open"
                );

                const expanded =
                    navigation.classList.contains(
                        "is-open"
                    );

                menuButton.setAttribute(
                    "aria-expanded",
                    expanded
                );
            }
        );
    }


    // =====================================================
    // BUSCADOR PÚBLICO DEL MOCKUP
    // =====================================================

    const searchForm =
        document.querySelector(
            "[data-search-form]"
        );

    if (searchForm) {

        searchForm.addEventListener(
            "submit",
            (event) => {

                event.preventDefault();

                const input =
                    searchForm.querySelector(
                        "input"
                    );

                const query =
                    input.value.trim();

                const target =
                    query
                        ? (
                            "./explorar.html?q="
                            + encodeURIComponent(
                                query
                            )
                        )
                        : "./explorar.html";

                window.location.href = target;
            }
        );
    }


    // =====================================================
    // MOSTRAR / OCULTAR CONTRASEÑA
    // =====================================================

    const passwordButtons =
        document.querySelectorAll(
            "[data-password-toggle]"
        );

    passwordButtons.forEach((button) => {

        button.addEventListener(
            "click",
            () => {

                const targetId =
                    button.getAttribute(
                        "data-password-toggle"
                    );

                const input =
                    document.getElementById(
                        targetId
                    );

                if (!input) {
                    return;
                }

                const showing =
                    input.type === "text";

                input.type =
                    showing
                        ? "password"
                        : "text";

                button.textContent =
                    showing
                        ? "Mostrar"
                        : "Ocultar";
            }
        );
    });


    // =====================================================
    // REGISTRO - TIPO DE USUARIO
    // =====================================================

    const userTypeInputs =
        document.querySelectorAll(
            'input[name="tipo_usuario"]'
        );

    const profileSections =
        document.querySelectorAll(
            "[data-profile-fields]"
        );


    function updateProfileFields() {

        if (
            !userTypeInputs.length ||
            !profileSections.length
        ) {
            return;
        }

        const selected =
            document.querySelector(
                'input[name="tipo_usuario"]:checked'
            );

        profileSections.forEach(
            (section) => {

                section.classList.remove(
                    "is-visible"
                );

                const fields =
                    section.querySelectorAll(
                        "input, select"
                    );

                fields.forEach(
                    (field) => {
                        field.disabled = true;
                    }
                );
            }
        );

        if (!selected) {
            return;
        }

        const target =
            document.querySelector(
                `[data-profile-fields="${selected.value}"]`
            );

        if (!target) {
            return;
        }

        target.classList.add(
            "is-visible"
        );

        const fields =
            target.querySelectorAll(
                "input, select"
            );

        fields.forEach(
            (field) => {
                field.disabled = false;
            }
        );
    }


    userTypeInputs.forEach((input) => {

        input.addEventListener(
            "change",
            updateProfileFields
        );
    });


    updateProfileFields();

        // =====================================================
    // SIDEBAR DE USUARIOS AUTENTICADOS
    // =====================================================

    const appMenuButton =
        document.querySelector(
            "[data-app-menu]"
        );

    const appSidebar =
        document.querySelector(
            "[data-app-sidebar]"
        );

    if (appMenuButton && appSidebar) {

        appMenuButton.addEventListener(
            "click",
            () => {

                appSidebar.classList.toggle(
                    "is-open"
                );

            }
        );
    }
});