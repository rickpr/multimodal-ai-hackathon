import { Container, Heading,} from "@chakra-ui/react"
import { createFileRoute } from "@tanstack/react-router"
import { useEffect, useRef, useState } from "react"

import TruthMeter from "../components/TruthMeter"

export const Route = createFileRoute("/video")({ component: PlayVideo })


interface Chunk {
  text: string
  truthiness: number
  timestamp: [number, number]
}

function PlayVideo () {
  const videoRef = useRef<HTMLVideoElement | null>(null)
  const [timer, setTimer] = useState<number | null>(null)
  const [chunks, setChunks] = useState<Chunk[] | null>(null)
  const [currentChunk, setCurrentChunk] = useState<Chunk | null>(null)
  useEffect(() => {
    const video = videoRef.current
    if (!video) return

    const timeUpdate = function () {
      setTimer(video.currentTime)
      if (chunks) {
        const chunk = chunks.find((chunk: any) => {
          return video.currentTime >= chunk.timestamp[0] && video.currentTime <= chunk.timestamp[1]
        })
        if (chunk) {
          setCurrentChunk(chunk)
        } else {
          setCurrentChunk(null)
        }
      }
    }
    videoRef.current?.addEventListener('timeupdate', timeUpdate)
    return () => videoRef.current?.removeEventListener('timeupdate', timeUpdate)
  }, [videoRef.current])

  useEffect(() => {
    const fetchChunks = async () => {
      const response = await fetch('/assets/json/output.json')
      const json = await response.json()
      setChunks(json)
    }
    fetchChunks()
  }, [])

  return (
    <Container maxW="full">
      <Heading size="lg" textAlign={{ base: "center", md: "left" }} pt={12}>
        Video
      </Heading>

      <video controls src='/assets/videos/highlights.webm' ref={videoRef} />
      {timer}
      {currentChunk?.text}
      {currentChunk && <TruthMeter value={currentChunk.truthiness} />}
    </Container>
  )
}
