function my_scope(){
    const forms = document.querySelectorAll('.form-delete');
    for (const form of forms) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const confirmed = confirm('Você confirma a exclusão da receita?')
            if (confirmed) {
                form.submit();
            }
        });
    }
}

my_scope();