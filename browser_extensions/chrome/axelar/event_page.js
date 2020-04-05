var contextMenuItem = {
    "id": "avsearch",
    "title": "Search Axelar",
    "contexts": ["image", "selection"]
};

chrome.contextMenus.create(contextMenuItem);
chrome.contextMenus.onClicked.addListener(function(clickData){
    if (clickData.menuItemId == "avsearch") {                               
        baseUrl = 'http://ec2-18-216-11-182.us-east-2.compute.amazonaws.com:7001/json';
        imageUrl = clickData.srcUrl;
        url = baseUrl + '/' + imageUrl;

        // Get request through Chrome API
        fetch(url).then(r => r.text()).then(result => {
            resultJson = JSON.parse(result)
            imageUrls = [];
            for (i = 0; i < resultJson.length; i++){
                imageUrls[i] = resultJson[i][2];
            }            
            chrome.storage.local.set({'matches': imageUrls});
        });
    }
});