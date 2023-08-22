import SignIn from '@/components/SignIn'
import useAuth from '@/utils/hooks/useAuth'
import Board from "@/components/Board";
//import styles from '@/styles/Home.module.css'

export default function Home() {
  const { authenticated } = useAuth()
  return <>{authenticated ? <Board /> : <SignIn />}</>
}
