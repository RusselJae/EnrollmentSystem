
$(document).ready(function() {
    // Subject Search Functionality
    $('.subject-search').on('input', function() {
        const searchTerm = $(this).val();
        const targetField = $(this);
        
        if (searchTerm.length < 2) return;

        $.ajax({
            url: '{% url "search_subjects" %}',
            method: 'GET',
            data: { 'term': searchTerm },
            success: function(response) {
                const resultsBody = $('#subjectSearchResults tbody');
                resultsBody.empty();

                response.forEach(function(subject) {
                    const row = `
                        <tr>
                            <td>${subject.sub_code}</td>
                            <td>${subject.sub_name}</td>
                            <td>${subject.lec_units}</td>
                            <td>${subject.lab_units}</td>
                            <td>
                                <button class="btn btn-sm btn-primary select-subject" 
                                        data-code="${subject.sub_code}"
                                        data-name="${subject.sub_name}"
                                        data-lec="${subject.lec_units}"
                                        data-lab="${subject.lab_units}"
                                        data-target="${targetField.attr('id')}">
                                    Select
                                </button>
                            </td>
                        </tr>
                    `;
                    resultsBody.append(row);
                });

                $('#subjectSearchModal').modal('show');
            }
        });
    });

    // Select Subject from Modal
    $(document).on('click', '.select-subject', function() {
        const targetId = $(this).data('target');
        const subjectCode = $(this).data('code');
        const subjectName = $(this).data('name');
        const lecUnits = $(this).data('lec');
        const labUnits = $(this).data('lab');

        $(`#${targetId}`).val(`${subjectCode} - ${subjectName}`);
        $(`#${targetId}_code`).val(subjectCode);
        $(`#lec${targetId.replace('subject', '')}`).val(lecUnits);
        $(`#lab${targetId.replace('subject', '')}`).val(labUnits);

        $('#subjectSearchModal').modal('hide');
    });

    // Clear Subject Search
    $('.subject-clear').on('click', function() {
        const targetId = $(this).data('target');
        $(`#${targetId}`).val('');
        $(`#${targetId}_code`).val('');
        $(`#lec${targetId.replace('subject', '')}`).val('');
        $(`#lab${targetId.replace('subject', '')}`).val('');
    });
});

