jQuery(document).ready(function($) {
    let tracks = [];
    
    // Character counter for genre textarea
    $('#genre').on('input', function() {
        const count = $(this).val().length;
        const counter = $('#genreCount');
        counter.text(count);
        
        if (count > 200) {
            counter.css('color', '#ff6b6b');
        } else if (count > 150) {
            counter.css('color', '#ffd93d');
        } else {
            counter.css('color', '#888');
        }
    });
    
    // Form submission
    $('#beatForm').on('submit', function(e) {
        e.preventDefault();
        generateBeat();
    });
    
    function generateBeat() {
        const $loading = $('#loading');
        const $result = $('#result');
        const $btn = $('.generate-btn');
        
        // Show loading state
        $loading.show();
        $result.hide();
        $btn.prop('disabled', true).text('🎵 Creating...');
        
        // Prepare form data
        const formData = {
            action: 'generate_beat',
            nonce: beatAddicts.nonce,
            prompt: $('#prompt').val(),
            genre: $('#genre').val(),
            mood: $('#mood').val(),
            duration: parseInt($('#duration').val())
        };
        
        // Make AJAX request
        $.ajax({
            url: beatAddicts.ajax_url,
            type: 'POST',
            data: formData,
            success: function(response) {
                if (response.success) {
                    displayResult(response.data);
                    addToTracksGrid(response.data);
                    $('#beatForm')[0].reset();
                    $('#genreCount').text('0');
                } else {
                    displayError('Generation failed. Please try again.');
                }
            },
            error: function() {
                displayError('Network error. Please check your connection.');
            },
            complete: function() {
                $loading.hide();
                $btn.prop('disabled', false).text('🎵 Drop the Beat');
            }
        });
    }
    
    function displayResult(song) {
        const $result = $('#result');
        const $songDetails = $('#songDetails');
        
        $songDetails.html(`
            <h4>${song.title}</h4>
            <p><strong>Genre:</strong> ${song.genre}</p>
            <p><strong>Mood:</strong> ${song.mood}</p>
            <p><strong>Duration:</strong> ${song.duration} seconds</p>
            <p><strong>Lyrics Preview:</strong></p>
            <div class="track-result">
                ${song.lyrics}
            </div>
            <p><strong>File:</strong> ${song.filename} (${song.file_size})</p>
            <audio controls style="width: 100%; margin: 15px 0;">
                <source src="${song.audio_url}" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
            <a href="${song.audio_url}" class="download-btn" download>
                🎧 Get Your Fix - ${song.filename}
            </a>
        `);
        
        $result.show();
    }
    
    function addToTracksGrid(song) {
        const $grid = $('#tracksGrid');
        const trackHtml = `
            <div class="track-card" data-id="${song.id}">
                <div class="track-header">
                    <div style="text-align: center; color: white; font-size: 24px;">🎵</div>
                </div>
                <div class="track-info">
                    <h3 class="track-title">${song.title}</h3>
                    <p class="track-prompt">${song.prompt}</p>
                    <audio controls style="width: 100%; margin-top: 10px;">
                        <source src="${song.audio_url}" type="audio/mpeg">
                    </audio>
                </div>
            </div>
        `;
        
        $grid.prepend(trackHtml);
        tracks.unshift(song);
    }
    
    function displayError(message) {
        const $result = $('#result');
        const $songDetails = $('#songDetails');
        
        $songDetails.html(`<p style="color: #ff6b6b;">Error: ${message}</p>`);
        $result.show();
    }
});
