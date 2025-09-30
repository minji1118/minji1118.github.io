exports.handler = async (event, context) => {
  return {
    statusCode: 200,
    body: JSON.stringify({message: "안녕! Node.js API에서 보낸 응답이야"})
  };
};
