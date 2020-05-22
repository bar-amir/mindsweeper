import fetch from 'isomorphic-unfetch'

// posts will be populated at build time by getStaticProps()
function Home({ sweeps }) {
  return (
    <div>
      <h1>Sweeps</h1>
      <ul>
        {sweeps.map(sweep => (
          <li>{sweep.sweepStart}</li>
        ))}
      </ul>
    </div>
  )
}

// This function gets called at build time on server-side.
// It won't be called on client-side, so you can even do
// direct database queries. See the "Technical details" section.
export async function getStaticProps() {
  // Call an external API endpoint to get posts.
  // You can use any data fetching library
  const res = await fetch('http://127.0.0.1:5000/users/42/sweeps')
  const sweeps = await res.json()

  // By returning { props: posts }, the Blog component
  // will receive `posts` as a prop at build time
  return {
    props: {
      sweeps,
    },
  }
}

export default Home