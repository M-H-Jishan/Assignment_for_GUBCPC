// Codeforces Contests Tracker
class ContestsTracker {
    constructor() {
        this.apiUrl = 'https://codeforces.com/api/contest.list';
        this.contests = [];
        this.filteredContests = [];
        this.currentFilter = 'upcoming';
        this.countdownIntervals = new Map();
        this.reminderTimers = new Map();
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.requestNotificationPermission();
        this.loadContests();
        
        // Update countdowns every second
        setInterval(() => this.updateCountdowns(), 1000);
    }
    
    setupEventListeners() {
        document.getElementById('refreshBtn').addEventListener('click', () => {
            this.loadContests();
        });
        
        document.getElementById('contestFilter').addEventListener('change', (e) => {
            this.currentFilter = e.target.value;
            this.filterAndDisplayContests();
        });
    }
    
    async requestNotificationPermission() {
        if ('Notification' in window) {
            const permission = await Notification.requestPermission();
            if (permission === 'granted') {
                this.showNotificationStatus();
            }
        }
    }
    
    showNotificationStatus() {
        const statusElement = document.getElementById('notificationStatus');
        statusElement.style.display = 'flex';
        setTimeout(() => {
            statusElement.style.display = 'none';
        }, 3000);
    }
    
    async loadContests() {
        this.showLoading();
        this.hideError();
        
        try {
            const response = await fetch(this.apiUrl);
            const data = await response.json();
            
            if (data.status === 'OK') {
                this.contests = data.result;
                this.filterAndDisplayContests();
            } else {
                throw new Error('Failed to fetch contests from Codeforces API');
            }
        } catch (error) {
            this.showError(`Error loading contests: ${error.message}`);
        } finally {
            this.hideLoading();
        }
    }
    
    filterAndDisplayContests() {
        const now = Date.now() / 1000; // Current time in seconds
        
        switch (this.currentFilter) {
            case 'upcoming':
                this.filteredContests = this.contests
                    .filter(contest => contest.phase === 'BEFORE')
                    .sort((a, b) => a.startTimeSeconds - b.startTimeSeconds);
                break;
                
            case 'past':
                this.filteredContests = this.contests
                    .filter(contest => contest.phase === 'FINISHED')
                    .sort((a, b) => b.startTimeSeconds - a.startTimeSeconds)
                    .slice(0, 5); // Show only last 5 past contests
                break;
                
            case 'all':
                this.filteredContests = this.contests
                    .sort((a, b) => {
                        // Sort by phase (upcoming first), then by start time
                        if (a.phase !== b.phase) {
                            const phaseOrder = { 'BEFORE': 0, 'CODING': 1, 'FINISHED': 2 };
                            return phaseOrder[a.phase] - phaseOrder[b.phase];
                        }
                        return a.startTimeSeconds - b.startTimeSeconds;
                    });
                break;
        }
        
        this.displayContests();
        this.updateSectionHeader();
    }
    
    displayContests() {
        const container = document.getElementById('contestsContainer');
        const template = document.getElementById('contestCardTemplate');
        
        // Clear existing contests
        container.innerHTML = '';
        
        if (this.filteredContests.length === 0) {
            container.innerHTML = `
                <div class="no-contests">
                    <i class="fas fa-calendar-times"></i>
                    <p>No contests found for the selected filter.</p>
                </div>
            `;
            return;
        }
        
        this.filteredContests.forEach(contest => {
            const contestCard = this.createContestCard(contest, template);
            container.appendChild(contestCard);
        });
    }
    
    createContestCard(contest, template) {
        const card = template.content.cloneNode(true);
        const cardElement = card.querySelector('.contest-card');
        
        // Set contest data
        card.querySelector('.contest-name').textContent = contest.name;
        card.querySelector('.contest-phase').textContent = this.getPhaseDisplay(contest.phase);
        card.querySelector('.contest-phase').className = `contest-phase phase-${contest.phase.toLowerCase()}`;
        
        // Format date and time
        const startDate = new Date(contest.startTimeSeconds * 1000);
        card.querySelector('.contest-date').textContent = this.formatDateTime(startDate);
        
        // Format duration
        const duration = this.formatDuration(contest.durationSeconds);
        card.querySelector('.contest-duration').textContent = duration;
        
        // Set contest link
        const contestLink = card.querySelector('.btn-link');
        contestLink.href = `https://codeforces.com/contest/${contest.id}`;
        
        // Handle countdown for upcoming contests
        if (contest.phase === 'BEFORE') {
            const countdownItem = card.querySelector('.countdown-item');
            const countdownTimer = card.querySelector('.countdown-timer');
            countdownItem.style.display = 'flex';
            
            // Store reference for countdown updates
            cardElement.dataset.contestId = contest.id;
            cardElement.dataset.startTime = contest.startTimeSeconds;
        } else {
            // Hide reminder button for past contests
            const reminderBtn = card.querySelector('.btn-reminder');
            reminderBtn.style.display = 'none';
        }
        
        // Store contest data for reminder functionality
        cardElement.dataset.contestData = JSON.stringify(contest);
        
        return card;
    }
    
    updateCountdowns() {
        const upcomingCards = document.querySelectorAll('[data-start-time]');
        
        upcomingCards.forEach(card => {
            const startTime = parseInt(card.dataset.startTime);
            const now = Math.floor(Date.now() / 1000);
            const timeLeft = startTime - now;
            
            const countdownElement = card.querySelector('.countdown-timer');
            if (countdownElement) {
                if (timeLeft > 0) {
                    countdownElement.textContent = this.formatCountdown(timeLeft);
                    countdownElement.parentElement.style.display = 'flex';
                } else {
                    countdownElement.textContent = 'Contest Started!';
                    countdownElement.parentElement.classList.add('contest-started');
                }
            }
        });
    }
    
    formatCountdown(seconds) {
        const days = Math.floor(seconds / 86400);
        const hours = Math.floor((seconds % 86400) / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        
        if (days > 0) {
            return `${days}d ${hours}h ${minutes}m`;
        } else if (hours > 0) {
            return `${hours}h ${minutes}m ${secs}s`;
        } else if (minutes > 0) {
            return `${minutes}m ${secs}s`;
        } else {
            return `${secs}s`;
        }
    }
    
    formatDateTime(date) {
        const options = {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            timeZoneName: 'short'
        };
        return date.toLocaleDateString('en-US', options);
    }
    
    formatDuration(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        
        if (hours > 0) {
            return `${hours}h ${minutes}m`;
        } else {
            return `${minutes}m`;
        }
    }
    
    getPhaseDisplay(phase) {
        const phases = {
            'BEFORE': 'Upcoming',
            'CODING': 'Live',
            'FINISHED': 'Finished'
        };
        return phases[phase] || phase;
    }
    
    updateSectionHeader() {
        const titleElement = document.getElementById('sectionTitle');
        const countElement = document.getElementById('contestCount');
        
        const titles = {
            'upcoming': 'Upcoming Contests',
            'past': 'Past Contests (Last 5)',
            'all': 'All Contests'
        };
        
        titleElement.textContent = titles[this.currentFilter];
        countElement.textContent = `${this.filteredContests.length} contest${this.filteredContests.length !== 1 ? 's' : ''}`;
    }
    
    showLoading() {
        document.getElementById('loadingSpinner').style.display = 'flex';
    }
    
    hideLoading() {
        document.getElementById('loadingSpinner').style.display = 'none';
    }
    
    showError(message) {
        const errorElement = document.getElementById('errorMessage');
        const errorText = document.getElementById('errorText');
        errorText.textContent = message;
        errorElement.style.display = 'flex';
    }
    
    hideError() {
        document.getElementById('errorMessage').style.display = 'none';
    }
}

// Reminder functionality
function setReminder(button) {
    const card = button.closest('.contest-card');
    const contestData = JSON.parse(card.dataset.contestData);
    
    if (!('Notification' in window)) {
        alert('This browser does not support notifications');
        return;
    }
    
    if (Notification.permission !== 'granted') {
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                scheduleReminder(contestData, button);
            } else {
                alert('Please enable notifications to set reminders');
            }
        });
    } else {
        scheduleReminder(contestData, button);
    }
}

function scheduleReminder(contest, button) {
    const startTime = contest.startTimeSeconds * 1000; // Convert to milliseconds
    const now = Date.now();
    const reminderTime = startTime - (15 * 60 * 1000); // 15 minutes before
    
    if (reminderTime <= now) {
        alert('Contest is starting too soon to set a reminder');
        return;
    }
    
    const timeUntilReminder = reminderTime - now;
    
    // Schedule the notification
    setTimeout(() => {
        new Notification('Codeforces Contest Reminder', {
            body: `"${contest.name}" starts in 15 minutes!`,
            icon: 'https://codeforces.org/s/0/favicon-96x96.png',
            tag: `contest-${contest.id}`,
            requireInteraction: true
        });
    }, timeUntilReminder);
    
    // Update button state
    button.innerHTML = '<i class="fas fa-check"></i> Reminder Set';
    button.classList.add('reminder-set');
    button.disabled = true;
    
    // Show confirmation
    showToast(`Reminder set for "${contest.name}" - 15 minutes before start`);
}

function showToast(message) {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `
        <i class="fas fa-check-circle"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(toast);
    
    // Show toast
    setTimeout(() => toast.classList.add('show'), 100);
    
    // Hide and remove toast
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => document.body.removeChild(toast), 300);
    }, 3000);
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    new ContestsTracker();
});
