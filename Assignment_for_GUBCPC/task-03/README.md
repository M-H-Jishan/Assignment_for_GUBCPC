# Codeforces Contests Tracker

A modern frontend application that fetches and displays upcoming programming contests from the Codeforces API with live countdown timers and browser notifications.

## Features

### Core Features
- **Live Contest Data**: Fetches real-time contest information from Codeforces API
- **Contest Information**: Displays contest name, local start time, and duration
- **Live Countdown**: Real-time countdown timers for upcoming contests
- **Browser Notifications**: Set reminders with 15-minute advance notifications
- **Contest Filtering**: Switch between upcoming, past (last 5), and all contests

### Additional Features
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Modern UI**: Clean, professional interface with smooth animations
- **Error Handling**: Graceful handling of API failures and network issues
- **Dark Mode Support**: Automatic dark mode based on system preferences
- **Toast Notifications**: User-friendly feedback for actions

## API Integration

The application uses the official Codeforces API:
- **Endpoint**: `https://codeforces.com/api/contest.list`
- **Documentation**: https://codeforces.com/apiHelp

## File Structure

```
task-03/
├── index.html          # Main HTML structure
├── styles.css          # Complete styling with responsive design
├── script.js           # JavaScript functionality and API integration
└── README.md           # This documentation
```

## Usage

### Opening the Application
1. Open `index.html` in a modern web browser
2. The application will automatically load upcoming contests
3. Grant notification permissions when prompted for reminder functionality

### Features Overview

#### Contest Display
- **Upcoming Contests**: Shows all future contests with countdown timers
- **Past Contests**: Displays the last 5 completed contests
- **All Contests**: Shows all contests sorted by status and time

#### Setting Reminders
1. Click "Set Reminder" on any upcoming contest
2. Grant notification permission if prompted
3. Receive a notification 15 minutes before the contest starts
4. Button will show "Reminder Set" after successful setup

#### Filtering Contests
Use the dropdown menu to switch between:
- **Upcoming Contests**: Future contests only
- **Past Contests**: Last 5 completed contests
- **All Contests**: Complete list

## Technical Details

### JavaScript Classes
- **ContestsTracker**: Main application class handling API calls and UI updates
- **Notification System**: Browser notification API integration
- **Countdown Timers**: Real-time countdown updates every second

### Key Functions
- `loadContests()`: Fetches data from Codeforces API
- `filterAndDisplayContests()`: Applies filters and updates display
- `updateCountdowns()`: Updates all countdown timers
- `setReminder()`: Schedules browser notifications
- `formatDateTime()`: Converts UTC to local time

### Responsive Breakpoints
- **Desktop**: > 768px (Grid layout)
- **Tablet**: 481px - 768px (Adjusted grid)
- **Mobile**: ≤ 480px (Single column)

## Browser Compatibility

### Supported Browsers
- Chrome 60+
- Firefox 55+
- Safari 11+
- Edge 79+

### Required Features
- Fetch API for HTTP requests
- Notification API for reminders
- ES6+ JavaScript features
- CSS Grid and Flexbox

## Error Handling

The application includes comprehensive error handling:
- **Network Errors**: Displays user-friendly error messages
- **API Failures**: Graceful degradation with retry options
- **Permission Denied**: Clear instructions for enabling notifications
- **Invalid Data**: Validates API responses before processing

## Performance Optimizations

- **Efficient DOM Updates**: Minimal DOM manipulation
- **Debounced API Calls**: Prevents excessive requests
- **Lazy Loading**: Only loads visible content
- **Optimized Animations**: Hardware-accelerated CSS transitions

## Customization

### Styling
Modify `styles.css` to customize:
- Color scheme (CSS variables in `:root`)
- Layout and spacing
- Animation timings
- Responsive breakpoints

### Functionality
Extend `script.js` to add:
- Additional contest platforms
- Custom notification timing
- Data persistence
- Advanced filtering options

## Troubleshooting

### Common Issues

**Contests not loading:**
- Check internet connection
- Verify Codeforces API is accessible
- Look for CORS issues in browser console

**Notifications not working:**
- Ensure browser supports Notification API
- Check notification permissions in browser settings
- Verify HTTPS connection (required for notifications)

**Countdown timers incorrect:**
- Verify system time is correct
- Check timezone settings
- Ensure JavaScript is enabled

### Browser Console
Open developer tools (F12) to check for:
- Network errors
- JavaScript errors
- API response issues

## Future Enhancements

Potential improvements:
- **Multiple Platforms**: Support for AtCoder, TopCoder, etc.
- **Calendar Integration**: Export contests to Google Calendar
- **User Preferences**: Customizable reminder timing
- **Contest History**: Track participation and performance
- **Offline Support**: Service worker for offline functionality

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.
