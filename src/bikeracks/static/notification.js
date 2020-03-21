const Notifications = (() => {
    return {
        // Options and settings for alerts
        // Success/error messages for submitting a bike rack removal suggestion
        suggestionErrorMessage: "Sorry, unable to send suggestion at this time.",
        suggestionSuccessMessage: "Suggestion sent. Thank you.",
        // Success/error messages for submitting feedback
        feedbackErrorMessage: "Sorry, unable to send feedback at this time.",
        feedbackSuccessMessage: "Thank you for your feedback.",
        // Success/error messages for voting on a bike rack
        voteErrorMessage: "Sorry, there was an error. Please try again later.",
        voteSuccessMessage: "Thank you for your vote.",
        // Success/error messages for submitting a bike rack
        submitBikeSuccess: "Thank you for adding a bike rack to the map.",
        submitBikeError: "Unable to add bike rack at this time. Please try again later.",
        errorIcon: 'glyphicon glyphicon-warning-sign',
        successIcon: 'glyphicon glyphicon-ok',
        renderMessage: (icon, message) => {
            return {
                icon,
                message
            }
        },
        errorSettings: {type: "danger"},
        successSettings: {type: "success"}
    }
})()



