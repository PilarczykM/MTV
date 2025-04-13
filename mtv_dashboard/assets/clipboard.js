window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clipboard: {
        copyUrlToClipboard: function(n_clicks) {
            const fullUrl = window.location.href;  // <-- to daje cały URL!
            if (!fullUrl) return "";
            navigator.clipboard.writeText(fullUrl).then(() => {
                console.log("URL copied:", fullUrl);
            });
            return "✅ URL copied to clipboard!";
        }
    }
});
