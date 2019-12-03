module Day2 where
import System.IO
import Data.List.Split
import Data.Array

runProgram :: Array Int Int -> Int -> Int
runProgram memory ip  
  | op == 1 = runProgram memory' (ip+4)
  | op == 2 = runProgram memory'' (ip+4)
  | otherwise = memory!0
  where memory'  = memory // [(addr3, ((memory!addr1) + (memory!addr2)))]
        memory'' = memory // [(addr3, ((memory!addr1) * (memory!addr2)))]
        addr1    = memory!(ip+1)
        addr2    = memory!(ip+2)
        addr3    = memory!(ip+3)
        op       = memory!ip

f :: [String] -> [Int]
f = map read

part1 :: Array Int Int -> Int
part1 mem = runProgram upd 0
  where upd = mem // [(1,12), (2,2)]

part2 mem = take 1 [ 100*noun+verb | 
        noun <- [0..99], verb <- [0..99], runProgram (upd noun verb) 0 == 19690720]
  where upd n v = mem // [(1,n), (2,v)]

main = do
    handle <- openFile "input2.txt" ReadMode
    contents <- hGetContents handle
    let code = f (splitOn "," contents)
        ln = (length code) - 1
        arr = array (0, ln) (zip [0..ln] code)
        p1 = part1 arr
        p2 = part2 arr
    print p1
    print p2
    hClose handle
    return ()
    
