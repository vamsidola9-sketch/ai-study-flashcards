document.getElementById('generateBtn').addEventListener('click', async () => {
    const notes = document.getElementById('notesInput').value.trim();
    if (!notes) {
        alert('Please paste some text notes first!');
        return;
    }

    const loadingEl = document.getElementById('loading');
    const containerEl = document.getElementById('flashcardsContainer');
    
    // Reset view states
    loadingEl.classList.remove('hidden');
    containerEl.innerHTML = '';

    try {
        // Send request payload to your python HTTP server endpoint
        const response = await fetch('http://localhost:5000/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ notes: notes })
        });

        const data = await response.json();

        if (data.success && data.flashcards) {
            renderFlashcards(data.flashcards);
        } else {
            alert('Failed generation error: ' + (data.error || 'Unknown server fault.'));
        }
    } catch (err) {
        console.error(err);
        alert('Could not hook into the backend server. Make sure your Python server is running on port 5000!');
    } finally {
        loadingEl.classList.add('hidden');
    }
});

function renderFlashcards(cards) {
    const container = document.getElementById('flashcardsContainer');
    
    cards.forEach(item => {
        const card = document.createElement('div');
        card.className = 'card';
        
        card.innerHTML = `
            <div class="card-inner">
                <div class="card-front">❓ ${item.question}</div>
                <div class="card-back">💡 ${item.answer}</div>
            </div>
        `;
        
        // Interactive Flip trigger binding
        card.addEventListener('click', () => {
            card.classList.toggle('flipped');
        });
        
        container.appendChild(card);
    });
}
