// Timesheet Views - Centralized JavaScript

// Notification System
function showNotification(message, type = 'info', duration = 5000) {
    const container = document.getElementById('notification-container');
    if (!container) return;

    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">${message}</div>
        <button class="notification-close" onclick="this.parentElement.remove()">&times;</button>
    `;

    container.appendChild(notification);

    // Auto-remove after duration
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, duration);
}

function closeNotification(button) {
    const notification = button.parentElement;
    if (notification) {
        notification.remove();
    }
}

// Modal Functions
function addEntry(date) {
    document.getElementById('modal-title').textContent = 'Add Entry';
    document.getElementById('entry-form').reset();
    document.getElementById('entry-date').value = date;
    document.getElementById('entry-id').value = '';
    clearValidationErrors();
    
    // Display the date in the modal
    const modalDateElement = document.getElementById('modal-date');
    if (modalDateElement) {
        const dateObj = new Date(date);
        const formattedDate = dateObj.toLocaleDateString('en-US', { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        });
        modalDateElement.textContent = formattedDate;
    }
    
    document.getElementById('entry-modal').style.display = 'block';
}

function editEntry(button) {
    const entryItem = button.closest('.entry-item');
    const entryId = entryItem.dataset.entryId;
    const projectName = entryItem.querySelector('.entry-project').textContent;
    const taskText = entryItem.querySelector('.entry-task').textContent;
    const hoursText = entryItem.querySelector('.entry-hours').textContent;
    const description = taskText.split(' - ')[1] || '';
    const taskCategory = taskText.split(' - ')[0] || '';

    document.getElementById('modal-title').textContent = 'Edit Entry';
    document.getElementById('entry-id').value = entryId;
    
    // Get the proper date from the calendar day element
    const calendarDay = entryItem.closest('.calendar-day');
    const dayEntries = calendarDay.querySelector('.day-entries');
    const properDate = dayEntries.id.replace('entries-', ''); // This gets the ISO date from the ID
    document.getElementById('entry-date').value = properDate;
    
    document.getElementById('entry-hours').value = parseFloat(hoursText);
    document.getElementById('entry-description').value = description;

    // Set project dropdown
    const projectSelect = document.getElementById('entry-project');
    for (let option of projectSelect.options) {
        if (option.text === projectName) {
            option.selected = true;
            break;
        }
    }

    // Set task category dropdown
    const taskSelect = document.getElementById('entry-task');
    for (let option of taskSelect.options) {
        if (option.text === taskCategory) {
            option.selected = true;
            break;
        }
    }

    clearValidationErrors();
    
    // Display the date in the modal
    const modalDateElement = document.getElementById('modal-date');
    if (modalDateElement) {
        const dateValue = document.getElementById('entry-date').value;
        const dateObj = new Date(dateValue);
        const formattedDate = dateObj.toLocaleDateString('en-US', { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        });
        modalDateElement.textContent = formattedDate;
    }
    
    document.getElementById('entry-modal').style.display = 'block';
}

function deleteEntry(button) {
    if (!confirm('Are you sure you want to delete this entry?')) {
        return;
    }

    const entryItem = button.closest('.entry-item');
    const entryId = entryItem.dataset.entryId;
    const dayElement = entryItem.closest('.day-entries');

    // Show loading overlay
    showLoading('Deleting entry...');

    fetch('/timesheet/delete-entry', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ entry_id: entryId })
    })
    .then(response => {
        hideLoading();
        if (response.ok) {
            entryItem.remove();
            updateDayTotal(dayElement);
            showNotification('Entry deleted successfully', 'success');
        } else {
            throw new Error('Failed to delete entry');
        }
    })
    .catch(error => {
        hideLoading();
        console.error('Error:', error);
        showNotification('Error deleting entry', 'error');
    });
}

function closeModal() {
    document.getElementById('entry-modal').style.display = 'none';
}

// Total Calculation Functions
function updateDayTotal(dayElement) {
    if (!dayElement) return;
    
    const entries = dayElement.querySelectorAll('.entry-item');
    let total = 0;
    
    entries.forEach(entry => {
        const hoursText = entry.querySelector('.entry-hours').textContent;
        const hours = parseFloat(hoursText) || 0;
        total += hours;
    });
    
    const dayHeader = dayElement.closest('.calendar-day').querySelector('.day-total');
    if (dayHeader) {
        dayHeader.textContent = total.toFixed(1) + 'h';
    }
    
    // Show/hide no entries message
    const noEntries = dayElement.querySelector('.no-entries');
    if (noEntries) {
        noEntries.style.display = entries.length === 0 ? 'block' : 'none';
    }
}

function updateWeekTotal() {
    const dayTotals = document.querySelectorAll('.day-total');
    let weekTotal = 0;
    
    dayTotals.forEach(dayTotal => {
        const hoursText = dayTotal.textContent;
        const hours = parseFloat(hoursText) || 0;
        weekTotal += hours;
    });
    
    const totalElement = document.getElementById('total-hours');
    if (totalElement) {
        totalElement.textContent = weekTotal.toFixed(1);
    }
    
    const avgElement = document.getElementById('daily-average');
    if (avgElement) {
        const average = weekTotal > 0 ? weekTotal / 7 : 0;
        avgElement.textContent = average.toFixed(1);
    }
}

function calculateAllDayTotals() {
    const dayEntries = document.querySelectorAll('.day-entries');
    dayEntries.forEach(dayElement => {
        updateDayTotal(dayElement);
    });
    updateWeekTotal();
}

// Form Submission
function handleEntrySubmit(event) {
    event.preventDefault();
    
    // Clear previous validation errors
    clearValidationErrors();
    
    const formData = new FormData(event.target);
    const data = {
        entry_id: formData.get('entry_id'),
        date: formData.get('date'),
        project_id: formData.get('project_id'),
        task_id: formData.get('task_id'),
        hours: formData.get('hours'),
        description: formData.get('description')
    };
    
    // Validate required fields
    const requiredFields = ['project_id', 'task_id', 'hours', 'description'];
    const missingFields = [];
    
    requiredFields.forEach(field => {
        const value = data[field];
        if (!value || value.trim() === '') {
            missingFields.push(field);
            highlightFieldError(field);
        }
    });
    
    if (missingFields.length > 0) {
        showNotification('Please fill in all required fields', 'error');
        return;
    }
    
    // Show loading overlay
    showLoading(data.entry_id ? 'Updating entry...' : 'Saving entry...');
    
    const url = data.entry_id ? '/timesheet/save-entry' : '/timesheet/save-entry';
    
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        hideLoading();
        if (result.success) {
            closeModal();
            showNotification(result.message, 'success');
            setTimeout(() => {
                location.reload();
            }, 1000);
        } else {
            showNotification(result.message || 'Error saving entry', 'error');
        }
    })
    .catch(error => {
        hideLoading();
        console.error('Error:', error);
        showNotification('Error saving entry', 'error');
    });
}

// Loading functionality
function showLoading(message = 'Saving entry...') {
    const overlay = document.getElementById('loading-overlay');
    const loadingText = document.getElementById('loading-text');
    const progressFill = document.getElementById('progress-fill');
    
    if (overlay && loadingText && progressFill) {
        loadingText.textContent = message;
        progressFill.style.width = '0%';
        overlay.classList.add('show');
        
        // Animate progress bar
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 90) progress = 90;
            progressFill.style.width = progress + '%';
        }, 200);
        
        // Store interval for cleanup
        overlay.dataset.progressInterval = progressInterval;
    }
}

function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    const progressFill = document.getElementById('progress-fill');
    
    if (overlay && progressFill) {
        // Complete the progress bar
        progressFill.style.width = '100%';
        
        // Clear the progress interval
        if (overlay.dataset.progressInterval) {
            clearInterval(parseInt(overlay.dataset.progressInterval));
        }
        
        // Hide after a short delay to show completion
        setTimeout(() => {
            overlay.classList.remove('show');
        }, 300);
    }
}

// Validation helper functions
function highlightFieldError(fieldName) {
    const field = document.getElementById(`entry-${fieldName}`);
    if (field) {
        field.style.borderColor = '#e53e3e';
        field.style.boxShadow = '0 0 0 1px #e53e3e';
    }
}

function clearValidationErrors() {
    const formFields = ['project', 'task', 'hours', 'description'];
    formFields.forEach(field => {
        const element = document.getElementById(`entry-${field}`);
        if (element) {
            element.style.borderColor = '#e2e8f0';
            element.style.boxShadow = 'none';
        }
    });
}

// Navigation Functions
function changeDate(selectedDate) {
    const currentUrl = new URL(window.location);
    currentUrl.searchParams.set('date', selectedDate);
    window.location.href = currentUrl.toString();
}

function jumpToToday() {
    const today = new Date().toISOString().split('T')[0];
    changeDate(today);
}

function jumpToDate(date) {
    changeDate(date);
}

// Voice Recognition functionality
let recognition = null;
let isRecording = false;

function initializeSpeechRecognition() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.continuous = true; // Enable continuous recording
        recognition.interimResults = true; // Get interim results for better UX
        recognition.lang = 'en-US';
        
        recognition.onstart = function() {
            isRecording = true;
            const voiceBtn = document.getElementById('voice-input-btn');
            const voiceStatus = document.getElementById('voice-status');
            if (voiceBtn) {
                voiceBtn.classList.add('recording');
                voiceBtn.querySelector('.voice-icon').textContent = '🔴';
                voiceBtn.title = 'Stop Voice Recording';
            }
            if (voiceStatus) {
                voiceStatus.textContent = 'Listening...';
                voiceStatus.classList.add('recording');
            }
            showNotification('Listening... Speak now!', 'info');
        };
        
        recognition.onresult = function(event) {
            let finalTranscript = '';
            let interimTranscript = '';
            
            // Combine all results for continuous recording
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript + ' ';
                } else {
                    interimTranscript += transcript;
                }
            }
            
            // Check if quick voice modal is open
            const quickModal = document.getElementById('quick-voice-modal');
            if (quickModal && quickModal.classList.contains('show')) {
                // Update quick voice modal with continuous transcript
                if (finalTranscript) {
                    quickVoiceTranscript = finalTranscript.trim();
                    document.getElementById('quick-voice-transcript').value = quickVoiceTranscript;
                } else if (interimTranscript) {
                    // Show interim results while recording
                    document.getElementById('quick-voice-transcript').value = quickVoiceTranscript + ' ' + interimTranscript;
                }
            } else {
                // Update regular modal
                const descriptionField = document.getElementById('entry-description');
                if (descriptionField) {
                    if (finalTranscript) {
                        descriptionField.value = finalTranscript.trim();
                    } else if (interimTranscript) {
                        descriptionField.value = descriptionField.value + ' ' + interimTranscript;
                    }
                    // Trigger validation
                    const inputEvent = new Event('input', { bubbles: true });
                    descriptionField.dispatchEvent(inputEvent);
                }
            }
        };
        
        recognition.onerror = function(event) {
            console.error('Speech recognition error:', event.error);
            showNotification('Voice recognition error: ' + event.error, 'error');
        };
        
        recognition.onend = function() {
            isRecording = false;
            const voiceBtn = document.getElementById('voice-input-btn');
            const voiceStatus = document.getElementById('voice-status');
            if (voiceBtn) {
                voiceBtn.classList.remove('recording');
                voiceBtn.querySelector('.voice-icon').textContent = '🎤';
                voiceBtn.title = 'Start Voice Recording';
            }
            if (voiceStatus) {
                voiceStatus.textContent = '';
                voiceStatus.classList.remove('recording');
            }
        };
    } else {
        console.warn('Speech recognition not supported in this browser');
    }
}

function toggleVoiceRecording() {
    if (!recognition) {
        showNotification('Voice recognition not supported in this browser', 'error');
        return;
    }
    
    const voiceBtn = document.getElementById('voice-input-btn');
    const voiceStatus = document.getElementById('voice-status');
    
    if (isRecording) {
        // Stop recording
        recognition.stop();
        if (voiceBtn) {
            voiceBtn.classList.remove('recording');
            voiceBtn.querySelector('.voice-icon').textContent = '🎤';
            voiceBtn.title = 'Start Voice Recording';
        }
        if (voiceStatus) {
            voiceStatus.textContent = '';
            voiceStatus.classList.remove('recording');
        }
        showNotification('Voice recording stopped', 'info');
    } else {
        // Start recording
        try {
            recognition.start();
            if (voiceBtn) {
                voiceBtn.classList.add('recording');
                voiceBtn.querySelector('.voice-icon').textContent = '🔴';
                voiceBtn.title = 'Stop Voice Recording';
            }
            if (voiceStatus) {
                voiceStatus.textContent = 'Recording...';
                voiceStatus.classList.add('recording');
            }
        } catch (error) {
            console.error('Error starting speech recognition:', error);
            showNotification('Error starting voice recognition', 'error');
        }
    }
}

// Keep the old function for backward compatibility
function startVoiceInput() {
    toggleVoiceRecording();
}

// Quick Voice Entry functionality
let quickVoiceTranscript = '';
let quickVoiceDate = '';

function startQuickVoiceEntry() {
    // Set today's date
    const today = new Date();
    const formattedDate = today.toLocaleDateString('en-US', { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    });
    
    quickVoiceDate = today.toISOString().split('T')[0]; // YYYY-MM-DD format
    quickVoiceTranscript = '';
    
                // Update modal content
            document.getElementById('quick-voice-date').textContent = formattedDate;
            document.getElementById('quick-voice-status').textContent = 'Fill in the details above, then click "Start Recording"';
            document.getElementById('quick-voice-transcript').value = '';
    
    // Reset form
    document.getElementById('quick-project').value = '';
    document.getElementById('quick-task').value = '';
    document.getElementById('quick-hours').value = '1.0';
    
    // Show modal
    document.getElementById('quick-voice-modal').classList.add('show');
    
    // Reset buttons
    document.getElementById('record-btn').style.display = 'inline-block';
    document.getElementById('save-btn').style.display = 'none';
}

function closeQuickVoiceModal() {
    document.getElementById('quick-voice-modal').classList.remove('show');
    if (isRecording) {
        recognition.stop();
    }
}

function toggleQuickVoiceRecording() {
    if (!recognition) {
        showNotification('Voice recognition not supported in this browser', 'error');
        return;
    }
    
    const recordBtn = document.getElementById('record-btn');
    const recordIcon = recordBtn.querySelector('.record-icon');
    const recordText = recordBtn.querySelector('.record-text');
    const statusElement = document.getElementById('quick-voice-status');
    
    if (isRecording) {
        // Stop recording
        recognition.stop();
        recordBtn.classList.remove('recording');
        recordIcon.textContent = '🎤';
        recordText.textContent = 'Start Recording';
        statusElement.textContent = 'Voice input captured! Click "Save Entry" to save.';
        document.getElementById('save-btn').style.display = 'inline-block';
        showNotification('Recording stopped!', 'info');
    } else {
        // Start recording
        try {
            recognition.start();
            recordBtn.classList.add('recording');
            recordIcon.textContent = '🔴';
            recordText.textContent = 'Stop Recording';
            statusElement.textContent = 'Recording... Speak your complete description, then click "Stop Recording"';
            showNotification('Recording started! Speak your complete description', 'info');
        } catch (error) {
            console.error('Error starting speech recognition:', error);
            showNotification('Error starting voice recognition', 'error');
        }
    }
}

function saveQuickVoiceEntry() {
    // Validate form fields
    const projectId = document.getElementById('quick-project').value;
    const taskId = document.getElementById('quick-task').value;
    const hours = document.getElementById('quick-hours').value;
    
    if (!projectId) {
        showNotification('Please select a project', 'error');
        document.getElementById('quick-project').focus();
        return;
    }
    
    if (!taskId) {
        showNotification('Please select a task category', 'error');
        document.getElementById('quick-task').focus();
        return;
    }
    
    if (!hours || hours <= 0) {
        showNotification('Please enter valid hours', 'error');
        document.getElementById('quick-hours').focus();
        return;
    }
    
    // Get description from textarea (allows both voice and manual input)
    const description = document.getElementById('quick-voice-transcript').value.trim();
    if (!description) {
        showNotification('Please enter a description (voice or manual)', 'error');
        document.getElementById('quick-voice-transcript').focus();
        return;
    }
    
    // Show loading
    showLoading('Saving voice entry...');
    
    // Create entry data with actual form values
    const data = {
        date: quickVoiceDate,
        project_id: projectId,
        task_id: taskId,
        hours: hours,
        description: description
    };
    
    // Save entry
    fetch('/timesheet/save-entry', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        hideLoading();
        if (result.success) {
            closeQuickVoiceModal();
            showNotification('Voice entry saved successfully!', 'success');
            setTimeout(() => {
                location.reload();
            }, 1000);
        } else {
            showNotification(result.message || 'Error saving voice entry', 'error');
        }
    })
    .catch(error => {
        hideLoading();
        console.error('Error:', error);
        showNotification('Error saving voice entry', 'error');
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize speech recognition
    initializeSpeechRecognition();
    
    // Auto-remove initial flash messages
    const notifications = document.querySelectorAll('.notification');
    notifications.forEach(notification => {
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
    });
    
    // Calculate initial totals
    calculateAllDayTotals();
    
    // Add form submit handler
    const entryForm = document.getElementById('entry-form');
    if (entryForm) {
        entryForm.addEventListener('submit', handleEntrySubmit);
    }
    
    // Close modal when clicking outside
    const modal = document.getElementById('entry-modal');
    if (modal) {
        modal.addEventListener('click', function(event) {
            if (event.target === modal) {
                closeModal();
            }
        });
    }
    
    // Close modal with Escape key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeModal();
        }
    });
}); 