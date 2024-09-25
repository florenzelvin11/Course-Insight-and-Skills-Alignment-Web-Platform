import React, { useEffect, useRef } from "react";
import * as d3 from "d3";
import cloud from "d3-cloud";

// https://github.com/LaraMi92/d3-playground/blob/ecb0ca457a8b028ce8edb248df0e72cc0c683fa6/wordcloud/wordcloud.js
//  For testing
export default function WordCloud(props) {
  const words = props.words;
  const ref = useRef();
  function draw(words, svg) {
    svg
      .append("g")
      .attr("transform", "translate(125,125)")
      .selectAll("text")
      .data(words)
      .enter()
      .append("text")
      .style("font-size", (d) => `${d.size}px`)
      .style("fill", () => `hsl(${Math.random() * 360}, 100%, 20%)`)
      .attr("text-anchor", "middle")
      .attr("transform", (d) => `translate(${[d.x, d.y]})`)
      .text((d) => d.text);
  }

  useEffect(() => {  
    const drawWordCloud = (words) => {
      if (words) {
        const svg = d3.select(ref.current);
        const layout = cloud()
          .size([250, 250])
          .words(words.map((d) => ({ text: d.name, size: (d.weight * 0.8) })))
          .padding(0)
          .rotate(() => ~~(Math.random() * 2) * 90)
          .fontSize((d) => d.size)
          .on("end", svg, draw);

        layout.start();
      } 
    };

    drawWordCloud(words);
  }, [words]);

  return <div><svg ref={ref} width={250} height={250} style={{margin: 'auto', display: 'block'}} /></div>;
}
