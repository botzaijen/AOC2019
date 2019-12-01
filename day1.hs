module Day1 where
import System.IO

calcFuel :: Integer -> Integer
calcFuel m = (m `div` 3) - 2

calcFuelRec :: Integer -> Integer
calcFuelRec m = if res <= 0 then 0 else res + calcFuelRec res
                where res = (m `div` 3) - 2 
    

f :: [String] -> [Integer]
f = map read

main = do
    handle <- openFile "input1.txt" ReadMode
    contents <- hGetContents handle
    let masses = f (lines contents)
        fuel = sum $ fmap calcFuel masses
        fuelRec = sum $ fmap calcFuelRec masses
    print fuel
    print fuelRec
    hClose handle
    return ()
    
