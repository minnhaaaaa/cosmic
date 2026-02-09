import React, { useState, useEffect } from "react"

function cn(...classes: (string | undefined | false)[]) {
  return classes.filter(Boolean).join(" ")
}

export function InteractiveGridPattern({
  squares = [24, 24],
  className,
  squaresClassName,
  ...props
}: InteractiveGridPatternProps) {
  const [hoveredSquare, setHoveredSquare] = useState<number | null>(null)
  const [viewport, setViewport] = useState({ width: 0, height: 0 })
  const [horizontal, vertical] = squares

  useEffect(() => {
    const handleResize = () => {
      setViewport({ width: window.innerWidth, height: window.innerHeight })
    }
    handleResize()
    window.addEventListener("resize", handleResize)
    return () => window.removeEventListener("resize", handleResize)
  }, [])

  if (!viewport.width || !viewport.height) return null

  const squareWidth = viewport.width / horizontal
  const squareHeight = viewport.height / vertical

  return (
    <svg
      width={viewport.width}
      height={viewport.height}
      className={cn("absolute inset-0 h-full w-full", className)}
      {...props}
    >
      {Array.from({ length: horizontal * vertical }).map((_, index) => {
        const x = (index % horizontal) * squareWidth
        const y = Math.floor(index / horizontal) * squareHeight
        return (
          <rect
            key={index}
            x={x}
            y={y}
            width={squareWidth}
            height={squareHeight}
            className={cn(
              "stroke-gray-400/30 transition-all duration-100 ease-in-out [&:not(:hover)]:duration-1000",
              hoveredSquare === index ? "fill-gray-300/30" : "fill-transparent",
              squaresClassName
            )}
            onMouseEnter={() => setHoveredSquare(index)}
            onMouseLeave={() => setHoveredSquare(null)}
          />
        )
      })}
    </svg>
  )
}
