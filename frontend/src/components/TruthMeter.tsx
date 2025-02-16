import { Box, Flex, Text } from '@chakra-ui/react'

interface TruthMeterProps {
  value: number // A value between 0 and 1 representing the "truthiness"
  label?: string // Optional label for the meter
}

function TruthMeter({ value, label }: TruthMeterProps) {
  // Clamp the value between 0 and 1
  const clampedValue = Math.max(0, Math.min(1, value))

  // Calculate the rotation angle.  0 -> -90 degrees, 1 -> 90 degrees
  const angle = -90 + clampedValue * 180

  return (
    <Box width="200px" height="100px" position="relative" overflow="hidden">
      {/* Background Arc (Green to Red) */}
      <Box
        position="absolute"
        top="0"
        left="0"
        width="200px"
        height="200px"
        borderRadius="full"
        borderWidth="10px"
        borderColor="transparent"
        borderTopColor="red.500" // Start with red
        borderRightColor="green.500"  // Transition to green
        transform="rotate(-90deg)" // Start the arc at the left
        transformOrigin="bottom"
        zIndex="1"
      />

      {/* Needle */}
      <Box
        position="absolute"
        bottom="0"
        left="50%"
        width="2px"
        height="100px"
        bg="black"
        transform={`translateX(-50%) rotate(${angle}deg)`}
        transformOrigin="bottom"
        zIndex="2"
      />

      {/* Center Circle */}
      <Box
        position="absolute"
        bottom="-10px"
        left="50%"
        transform="translateX(-50%)"
        width="20px"
        height="20px"
        borderRadius="full"
        bg="gray.300"
        zIndex="3"
      />


      {/* Label (Optional) */}
      {label && (
        <Text textAlign="center" mt="2">
          {label}
        </Text>
      )}

      {/* Min/Max Labels */}
      <Flex justifyContent="space-between" width="100%" px="2">
        <Text fontSize="sm">False</Text>
        <Text fontSize="sm">True</Text>
      </Flex>

    </Box>
  )
}

export default TruthMeter
