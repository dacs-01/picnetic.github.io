
//~~~~~~~~~~~GRID SETUP~~~~~~~~~~~~~~~~
const container = document.querySelector('.container');

function buildHome(columns, posts){
    //clear the homepage every time index is opened, so we can rebuild it.
    container.innerHTML =''; 

    //container for each column of photos
    let columnStalls = {};

    for(let i = 0; i < columns; i++ ){
        columnStalls[`column${i}`] = []
    }

    for(let i = 0; i<posts.length; i++){
        //divide posts into columns and add to column stalls
        const columnNum = i %  columns;
        columnStalls[`column${columnNum}`].push(posts[i]);
    }
    
    for(let i = 0; i < columns; i++){
        let columnPosts = columnStalls[`columnNum${i}`];
        //add our div for our columns
        let colDiv = document.createElement('div');
        colDiv.classList.add('column');

        columnPosts.forEach(post => {
            //add div for each post & its image
            let postDiv = document.createElement('div');
            postDiv.classList.add('post');
            let image = document.createElement('img');
            image.src = post.image;
            let overlay = document.createElement('div');
            overlay.classList.add('overlay');
            
            overlay.appendChild(caption);
            postDiv.appendChild(image, overlay);
            colDiv.appendChild(postDiv);
        })
        container.appendChild(columnPosts);
    }
}
    buildHome(3, posts);
