window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clipboard: {
        copyStateUrlToClipboard: function (url) {
            if (!url) return "";
            const fullUrl = window.location.origin + window.location.pathname + url;
            navigator.clipboard.writeText(fullUrl).then(() => {
                console.log("Copied to clipboard:", fullUrl);
            });
            return "";
        }
    }
});
