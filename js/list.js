
class Activity {
  constructor(name, group, category, time) {
    this.name = name; //name of prg
    this.group = group; // e.g. chrome, vs code 
    this.category = category;//e.g. social, game, productivity, Entertainment
    this.time = time; // time spent

  }


  render_button() {
    return `
        <button type="button" class="collapsible">${this.name}<a style="float:right;" id="${this.name}">${this.time}</a></button>
	      <div class="content" id="${this.group}">
`;
  }
  render_div() {
    return `
		    <p>${this.name}<a style="float:right;">${this.time}</a></p>

`;
  }

  render_time() {
    return `
        ${this.time}
`;
  }

}

var heading = [
  new Activity("Others", 0, "", 0),
  new Activity("Chrome", 1, "", 0),
  new Activity("Visual Studio Code", 2, "", 0),
]
// name, group, category, time
var line = [
  new Activity("L.js", 2, "", 1),
]


function read_from_json() {
  // load the data
  d3.json("activities.json", function (error, data) {
    data = data.activities
    data.forEach(function (d) {
      d.Freq = Math.floor((d.total_time % 3600) / 60);
      line.push(new Activity(d.name, d.group, "", d.Freq));
      console.log(line.length)
    });

    getall()

  });

}


function getall() {
  completed_content.innerHTML = null;

  heading.forEach(heading => {
    completed_content.innerHTML += heading.render_button();
    let div = document.getElementById(heading.group);
    console.log("first")
    var x = line.filter(line => line.group == heading.group);
    var total = 0;

    x.forEach(filtered => {
      
      total += filtered.time;
      div.innerHTML += filtered.render_div(); //renders the entries line by line
    })

    heading.time = total;
    let update_total = document.getElementById(heading.name);
    update_total.innerHTML = heading.render_time();


  });
  var coll = document.getElementsByClassName("collapsible");
  var i;

  for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function () {
      console.log("clicked")
      this.classList.toggle("active");
      var content = this.nextElementSibling;
      if (content.style.display === "block") {
        content.style.display = "none";
      } else {
        content.style.display = "block";
      }
    });
  }
}




window.onload = () => {
  let completed_content = document.getElementById("completed_content");

  read_from_json()


}